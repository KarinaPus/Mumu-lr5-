from datetime import timedelta

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Exhibit, Exhibition, Guide, Hall, Museum, Profile, PromoCode, Review, Ticket, Tour, Visitor


class MuseumViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.museum = Museum.objects.create(
            name="Государственный музей",
            city="Москва",
            address="Тверская 12",
            description="Пример музея",
        )
        self.guide = Guide.objects.create(name="Иван Иванов", specialization="История", email="ivan@example.com")
        self.exhibition = Exhibition.objects.create(
            museum=self.museum,
            title="Старые экспонаты",
            description="Тестовая выставка",
            start_date="2024-01-01",
            end_date="2024-01-10",
        )
        self.exhibition.guides.add(self.guide)

    def test_home_page_works(self):
        response = self.client.get(reverse("museum:home"))
        self.assertEqual(response.status_code, 200)

    def test_exhibition_list(self):
        response = self.client.get(reverse("museum:exhibition-list"))
        self.assertEqual(response.status_code, 200)

    def test_booking_requires_auth(self):
        response = self.client.get(reverse("museum:booking"))
        self.assertEqual(response.status_code, 302)

    def test_register_and_create_ticket(self):
        user = User.objects.create_user(username="newuser", password="pass1234")
        visitor = Visitor.objects.create(user=user, phone="+70000000000")
        ticket = Ticket.objects.create(visitor=visitor, exhibition=self.exhibition)
        self.assertEqual(ticket.status, "booked")

    def test_api_requires_authentication(self):
        response = self.client.get("/api/museums/")
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_delete_exhibition(self):
        superuser = User.objects.create_superuser(username="admin2", password="pass1234", email="admin2@example.com")
        self.client.force_login(superuser)

        response = self.client.post(reverse("museum:exhibition-delete", args=[self.exhibition.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Exhibition.objects.filter(pk=self.exhibition.pk).exists())

    def test_superuser_sees_logout_and_delete_controls(self):
        superuser = User.objects.create_superuser(username="admin3", password="pass1234", email="admin3@example.com")
        self.client.force_login(superuser)

        home_response = self.client.get(reverse("museum:home"))
        detail_response = self.client.get(reverse("museum:exhibition-detail", args=[self.exhibition.pk]))

        self.assertEqual(home_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(home_response, 'class="logout-btn"')
        self.assertContains(detail_response, 'Удалить')

    def test_logged_in_user_can_upload_image_with_review(self):
        user = User.objects.create_user(username="reviewer", password="pass1234")
        self.client.force_login(user)

        image = SimpleUploadedFile("review.jpg", b"fake-image-content", content_type="image/jpeg")
        response = self.client.post(
            reverse("museum:review-create"),
            {
                "rating": 5,
                "text": "Очень понравилось!",
                "image": image,
            },
        )

        self.assertEqual(response.status_code, 302)
        review = Review.objects.get(author_name=user.get_full_name() or user.username)
        self.assertTrue(review.image)

        reviews_response = self.client.get(reverse("museum:reviews"))
        self.assertContains(reviews_response, 'img')

    def test_review_rating_cannot_exceed_five(self):
        user = User.objects.create_user(username="reviewer2", password="pass1234")
        self.client.force_login(user)

        response = self.client.post(
            reverse("museum:review-create"),
            {
                "rating": 6,
                "text": "Слишком высокий рейтинг",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("rating", response.context["form"].errors)

    def test_superuser_can_view_admin_statistics_report(self):
        superuser = User.objects.create_superuser(username="admin4", password="pass1234", email="admin4@example.com")
        self.client.force_login(superuser)

        hall = Hall.objects.create(
            museum=self.museum,
            number=2,
            name="Основной зал",
            floor=2,
            area=120.5,
        )
        guide = Guide.objects.create(
            name="Мария Петрова",
            specialization="Смотритель",
            phone="+79990001122",
            position="Старший смотритель",
            hall=hall,
        )
        Exhibit.objects.create(
            hall=hall,
            title="Роспись века",
            kind="Живопись",
            accession_date=timezone.now().date() - timedelta(days=30),
            assigned_guide=guide,
        )
        Tour.objects.create(
            museum=self.museum,
            title="Утро в музее",
            description="Экскурсия утренней группы",
            date=timezone.now().date().replace(month=7, day=1),
            participants=15,
            code="TOUR-001",
        )

        response = self.client.get(
            reverse("museum:stats"),
            {"floor": 2, "season": "summer", "date": (timezone.now().date() - timedelta(days=60)).isoformat()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Информация о залах")
        self.assertContains(response, "Основной зал")
        self.assertContains(response, "Мария Петрова")
        self.assertContains(response, "Роспись века")
        self.assertContains(response, "TOUR-001")
        self.assertContains(response, "Экспонаты по залам после выбранной даты")

    def test_visitor_cabinet_shows_purchases_and_promocodes(self):
        user = User.objects.create_user(username="visitor1", password="pass1234", first_name="Иван", last_name="Посетитель")
        visitor = Visitor.objects.create(user=user, phone="+79990001111")
        Profile.objects.create(user=user, role="visitor")
        Ticket.objects.create(visitor=visitor, exhibition=self.exhibition, status="booked")
        PromoCode.objects.create(code="SAVE10", description="Скидка 10%", discount=10, is_active=True)

        self.client.force_login(user)
        response = self.client.get(reverse("museum:cabinet"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Промокоды")
        self.assertContains(response, "SAVE10")
        self.assertContains(response, self.exhibition.title)

    def test_employee_cabinet_shows_assigned_exhibits_and_tours(self):
        user = User.objects.create_user(username="employee1", password="pass1234", first_name="Мария", last_name="Сотрудник")
        Profile.objects.create(user=user, role="employee")
        guide = Guide.objects.create(
            name="Мария Сотрудник",
            specialization="Смотритель",
            phone="+79990002222",
            position="Старший смотритель",
        )
        exhibit = Exhibit.objects.create(
            hall=self.exhibition.museum.halls.first() if self.exhibition.museum.halls.exists() else Hall.objects.create(
                museum=self.museum,
                number=1,
                name="Входной зал",
                floor=1,
                area=50,
            ),
            title="Золотой век",
            kind="Живопись",
            accession_date=timezone.now().date() - timedelta(days=15),
            assigned_guide=guide,
        )
        tour = Tour.objects.create(
            museum=self.museum,
            title="Экскурсия для сотрудников",
            description="Служебная экскурсия",
            date=timezone.now().date() + timedelta(days=5),
            participants=10,
            code="EMP-01",
        )
        tour.guides.add(guide)

        self.client.force_login(user)
        response = self.client.get(reverse("museum:cabinet"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Закрепленные экспонаты")
        self.assertContains(response, exhibit.title)
        self.assertContains(response, "Проводимые экскурсии")
        self.assertContains(response, tour.title)

    def test_api_token_authentication(self):
        user = User.objects.create_user(username="apiuser", password="pass1234")
        token = Token.objects.create(user=user)

        client = APIClient()
        token_response = client.post(
            reverse("museum:api-token"),
            {"username": "apiuser", "password": "pass1234"},
            format="json",
        )

        self.assertEqual(token_response.status_code, 200)
        self.assertEqual(token_response.data["token"], token.key)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        api_response = client.get("/api/museums/")
        self.assertEqual(api_response.status_code, 200)
