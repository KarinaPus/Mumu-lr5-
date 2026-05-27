from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Museum(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Hall(models.Model):
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, related_name="halls")
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=120)
    floor = models.PositiveIntegerField()
    area = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.museum.name} • Зал {self.number}"


class Guide(models.Model):
    name = models.CharField(max_length=120)
    specialization = models.CharField(max_length=120)
    position = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True, related_name="guides")
    photo = models.FileField(upload_to="", blank=True, default="a.jpg")

    def __str__(self):
        return self.name


class Exhibit(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="exhibits")
    title = models.CharField(max_length=200)
    kind = models.CharField(max_length=120)
    accession_date = models.DateField()
    description = models.TextField(blank=True)
    assigned_guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True, blank=True, related_name="supervised_exhibits")
    image = models.FileField(upload_to="", blank=True, default="12.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Exhibition(models.Model):
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, related_name="exhibitions")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    guides = models.ManyToManyField(Guide, blank=True, related_name="exhibitions")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.museum.name})"


class Tour(models.Model):
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, related_name="tours")
    code = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    participants = models.PositiveIntegerField(default=0)
    guides = models.ManyToManyField(Guide, blank=True, related_name="tours")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    image = models.FileField(upload_to="", blank=True, default="3.webp")
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class CompanyInfo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    history = models.TextField(blank=True)
    requisites = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    visitor = models.ForeignKey("Visitor", on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    author_name = models.CharField(max_length=120, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField()
    image = models.FileField(upload_to="reviews/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name or 'Аноним'}: {self.rating}"


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class TicketPrice(models.Model):
    DAY_CHOICES = (
        ("weekday", "Будни"),
        ("weekend", "Выходные"),
        ("holiday", "Праздник"),
    )
    AGE_CHOICES = (
        ("adult", "Взрослый"),
        ("child", "Детский"),
        ("student", "Студент"),
    )

    day_type = models.CharField(max_length=20, choices=DAY_CHOICES)
    age_group = models.CharField(max_length=20, choices=AGE_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_day_type_display()} / {self.get_age_group_display()}: {self.price}"


class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="visitor")
    phone = models.CharField(max_length=30, blank=True)
    favorite_museum = models.ForeignKey(Museum, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.get_username()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=50, default="visitor")
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Ticket(models.Model):
    STATUS_CHOICES = (
        ("booked", "Забронирован"),
        ("paid", "Оплачен"),
        ("used", "Использован"),
        ("cancelled", "Отменён"),
    )

    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name="tickets")
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, related_name="tickets")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="booked")

    def __str__(self):
        return f"{self.visitor.user.username} -> {self.exhibition.title}"
