from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from museum.models import (
    CompanyInfo,
    Exhibit,
    Exhibition,
    FAQ,
    Guide,
    Hall,
    Museum,
    NewsArticle,
    PromoCode,
    Review,
    TicketPrice,
    Tour,
    Vacancy,
)


class Command(BaseCommand):
    help = "Заполняет демонстрационные данные для музея"

    def handle(self, *args, **options):
        museum, _ = Museum.objects.get_or_create(
            name="Государственный музей",
            defaults={
                "city": "Москва",
                "address": "Тверская 12",
                "description": "Музей с постоянными экспозициями и тематическими выставками.",
            },
        )

        hall_1, _ = Hall.objects.get_or_create(
            museum=museum,
            number=1,
            defaults={
                "name": "Зал древностей",
                "floor": 1,
                "area": 120.0,
                "description": "История и предметы древности.",
            },
        )
        hall_2, _ = Hall.objects.get_or_create(
            museum=museum,
            number=2,
            defaults={
                "name": "Зал живописи",
                "floor": 2,
                "area": 150.0,
                "description": "Картины и живописные серии.",
            },
        )
        hall_3, _ = Hall.objects.get_or_create(
            museum=museum,
            number=3,
            defaults={
                "name": "Зал современного искусства",
                "floor": 3,
                "area": 130.0,
                "description": "Современные экспозиции и инсталляции.",
            },
        )

        guide_1, _ = Guide.objects.get_or_create(
            name="Иван Иванов",
            defaults={
                "specialization": "История",
                "email": "ivan@example.com",
                "phone": "+375 (29) 111-22-33",
                "description": "Проводит экскурсии по древним экспонатам.",
            },
        )
        guide_2, _ = Guide.objects.get_or_create(
            name="Ольга Петрова",
            defaults={
                "specialization": "Живопись",
                "email": "olga@example.com",
                "phone": "+375 (29) 222-33-44",
                "description": "Эксперт по экспозициям живописи.",
            },
        )
        guide_3, _ = Guide.objects.get_or_create(
            name="Сергей Орлов",
            defaults={
                "specialization": "Современное искусство",
                "email": "sergey@example.com",
                "phone": "+375 (29) 333-44-55",
                "description": "Проводит тематические экскурсии.",
            },
        )

        Exhibit.objects.get_or_create(
            hall=hall_1,
            title="Скифский кубок",
            defaults={
                "kind": "Древность",
                "accession_date": timezone.now().date() - timedelta(days=365),
                "description": "Редкий керамический сосуд с орнаментом.",
            },
        )
        Exhibit.objects.get_or_create(
            hall=hall_2,
            title="Пейзаж на закате",
            defaults={
                "kind": "Живопись",
                "accession_date": timezone.now().date() - timedelta(days=240),
                "description": "Картина в теплой цветовой гамме.",
            },
        )
        Exhibit.objects.get_or_create(
            hall=hall_3,
            title="Инсталляция света",
            defaults={
                "kind": "Современное искусство",
                "accession_date": timezone.now().date() - timedelta(days=120),
                "description": "Световая инсталляция для интерактивных экскурсий.",
            },
        )
        exhibit_data = [
            (hall_1, "Каменная утварь", "Древность", timezone.now().date() - timedelta(days=330), "Повседневные предметы древних мастеров.", "10.jpg"),
            (hall_1, "Глиняная посуда", "Древность", timezone.now().date() - timedelta(days=290), "Сборник керамики для хранения и приготовления пищи.", "12.jpg"),
            (hall_2, "Летний пейзаж", "Живопись", timezone.now().date() - timedelta(days=210), "Картина с естественной световой композицией.", "4.jpg"),
            (hall_2, "Портрет в золоте", "Живопись", timezone.now().date() - timedelta(days=180), "Портретный цикл с декоративными элементами.", "5.jpg"),
            (hall_2, "Натюрморт с цветами", "Живопись", timezone.now().date() - timedelta(days=150), "Композиция из цветов и предметов быта.", "8.jpg"),
            (hall_3, "Световой лабиринт", "Современное искусство", timezone.now().date() - timedelta(days=90), "Интерактивная инсталляция для детей и взрослых.", "10.jpg"),
            (hall_3, "Звуковая композиция", "Современное искусство", timezone.now().date() - timedelta(days=60), "Экспозиция, основанная на акустических эффектах.", "4.jpg"),
        ]
        for hall, title, kind, accession_date, description, image in exhibit_data:
            Exhibit.objects.get_or_create(
                hall=hall,
                title=title,
                defaults={
                    "kind": kind,
                    "accession_date": accession_date,
                    "description": description,
                    "image": image,
                },
            )

        exhibition_1, _ = Exhibition.objects.get_or_create(
            museum=museum,
            title="Весенняя выставка",
            defaults={
                "description": "Тематическая выставка в зале древностей.",
                "start_date": timezone.now().date() - timedelta(days=10),
                "end_date": timezone.now().date() + timedelta(days=20),
                "is_active": True,
            },
        )
        exhibition_2, _ = Exhibition.objects.get_or_create(
            museum=museum,
            title="Парад картин",
            defaults={
                "description": "Сборник живописных работ.",
                "start_date": timezone.now().date() - timedelta(days=30),
                "end_date": timezone.now().date() + timedelta(days=15),
                "is_active": True,
            },
        )
        exhibition_1.guides.set([guide_1])
        exhibition_2.guides.set([guide_2, guide_3])

        Tour.objects.get_or_create(
            museum=museum,
            title="Экскурсия по залам",
            defaults={
                "description": "Групповая экскурсия на текущей неделе.",
                "date": timezone.now().date() + timedelta(days=3),
                "participants": 12,
            },
        )
        Tour.objects.get_or_create(
            museum=museum,
            title="Летняя обзорная поездка",
            defaults={
                "description": "Обзорная экскурсия для школьников.",
                "date": timezone.now().date() + timedelta(days=8),
                "participants": 18,
            },
        )

        NewsArticle.objects.get_or_create(
            slug="novost-dnya-1",
            defaults={
                "title": "Новая выставка открыта",
                "summary": "В музее открылась новая выставка, посвящённая современному искусству.",
                "body": "Текст новости для демонстрации и наполнения сайта.",
                "published_at": timezone.now() - timedelta(days=1),
            },
        )
        NewsArticle.objects.get_or_create(
            slug="novost-dnya-2",
            defaults={
                "title": "Новые экскурсии для школьников",
                "summary": "Групповые экскурсии теперь доступны по субботам.",
                "body": "Подробнее о новых форматах и расписании мероприятий.",
                "published_at": timezone.now() - timedelta(days=3),
            },
        )
        NewsArticle.objects.get_or_create(
            slug="novost-dnya-3",
            defaults={
                "title": "Новый гид-практикант",
                "summary": "В музей поступил новый сотрудник для поддержки экскурсий.",
                "body": "Новая команда расширяет возможности музея.",
                "published_at": timezone.now() - timedelta(days=5),
            },
        )

        FAQ.objects.get_or_create(
            question="Как получить билеты?",
            defaults={
                "answer": "Билеты можно приобрести на странице бронирования или в кассе музея.",
            },
        )
        FAQ.objects.get_or_create(
            question="Есть ли скидки для студентов?",
            defaults={
                "answer": "Да, скидки доступны по действующим промокодам.",
            },
        )
        FAQ.objects.get_or_create(
            question="Можно ли заказать экскурсию?",
            defaults={
                "answer": "Да, экскурсии можно забронировать через раздел экскурсии.",
            },
        )

        CompanyInfo.objects.get_or_create(
            title="О музее",
            defaults={
                "description": "Наш музей посвящён истории, искусству и культурному наследию.",
                "history": "Основан в 1998 году, развивается по направлениям выставок и экскурсий.",
                "requisites": "ИП Музей, УНП 100000000, г. Москва, ул. Тверская, 12.",
            },
        )

        Vacancy.objects.get_or_create(
            title="Экскурсовод",
            defaults={
                "description": "Требуются опытные экскурсоводы для ведения групповых посещений.",
                "is_active": True,
            },
        )
        Vacancy.objects.get_or_create(
            title="Менеджер по продажам",
            defaults={
                "description": "Поддержка клиентов и работа с билетными запросами.",
                "is_active": True,
            },
        )

        PromoCode.objects.get_or_create(
            code="MUSEUM10",
            defaults={
                "description": "Скидка 10% на билеты для взрослых.",
                "discount": 10,
                "is_active": True,
                "valid_from": timezone.now().date() - timedelta(days=10),
                "valid_to": timezone.now().date() + timedelta(days=30),
            },
        )
        PromoCode.objects.get_or_create(
            code="STUDENT5",
            defaults={
                "description": "Скидка 5% для студентов.",
                "discount": 5,
                "is_active": False,
                "valid_from": timezone.now().date() - timedelta(days=30),
                "valid_to": timezone.now().date() - timedelta(days=5),
            },
        )

        TicketPrice.objects.get_or_create(
            day_type="weekday",
            age_group="adult",
            defaults={"price": 20.0},
        )
        TicketPrice.objects.get_or_create(
            day_type="weekend",
            age_group="adult",
            defaults={"price": 25.0},
        )
        TicketPrice.objects.get_or_create(
            day_type="child",
            age_group="child",
            defaults={"price": 10.0},
        )

        Review.objects.get_or_create(
            author_name="Анна",
            defaults={
                "rating": 5,
                "text": "Очень интересная выставка и приятная атмосфера.",
            },
        )
        Review.objects.get_or_create(
            author_name="Игорь",
            defaults={
                "rating": 4,
                "text": "Понравилась организация и экскурсии.",
            },
        )

        self.stdout.write(self.style.SUCCESS("Демо-данные успешно заполнены"))
