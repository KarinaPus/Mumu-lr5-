from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

class Museum(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


def validate_age_18_plus(value):
    """Проверяет, что возраст >= 18 лет"""
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError('Возраст должен быть 18 лет или старше.')



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
    birth_date = models.DateField(null=True, blank=True, validators=[validate_age_18_plus], verbose_name="Дата рождения")

    def __str__(self):
        return self.name
    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None


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
    is_adult_only = models.BooleanField(default=False, verbose_name="Только для 18+")

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
    birth_date = models.DateField(null=True, blank=True, validators=[validate_age_18_plus], verbose_name="Дата рождения")
    
    is_parent = models.BooleanField(default=False, verbose_name="Законный представитель")
    # children = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='parents', verbose_name="Дети")

    def __str__(self):
        return self.user.get_username()
    
    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username


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
    
    VISITOR_TYPE_CHOICES = (
        ("adult", "Взрослый"),
        ("child", "Ребенок/школьник"),
    )

    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name="tickets")
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, related_name="tickets")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="booked")
    visitor_type = models.CharField(max_length=10, choices=VISITOR_TYPE_CHOICES, default='adult', verbose_name="Тип посетителя")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Цена билета")
    
    child_visitor = models.ForeignKey(
        'Child', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tickets',
        verbose_name="Ребенок"
    )

    def __str__(self):
        child_info = f" (для {self.child_visitor.first_name})" if self.child_visitor else ""
        return f"{self.visitor.user.username} -> {self.exhibition.title}{child_info}"



class Child(models.Model):
    """Модель для детей (льготные билеты)"""
    parent = models.ForeignKey(
        'Visitor', 
        on_delete=models.CASCADE, 
        related_name="children"
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or f"Ребенок #{self.id}"
    
    @property
    def age(self):
        from datetime import date
        if self.birth_date:
            today = date.today()
            age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
            return age
        return None
    
    class Meta:
        verbose_name = "Ребенок"
        verbose_name_plural = "Дети"