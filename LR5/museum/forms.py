from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Exhibition, Review
from .models import Visitor, Guide
from datetime import date 
from .models import Exhibition, Review, Visitor, Profile, Child 


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=30, required=False, label="Телефон")
    birth_date = forms.DateField(
        required=True,
        label="Дата рождения",
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="ДД.ММ.ГГГГ (только для лиц от 18 лет)"
    )
    
    # Согласие с условиями
    agree_terms = forms.BooleanField(
        required=True,
        label="Я подтверждаю, что мне есть 18 лет, и я принимаю условия использования сайта"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "phone", "birth_date", "agree_terms"]

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            
            if age < 18:
                raise forms.ValidationError(
                    '⚠️ Регистрация на сайте доступна только лицам от 18 лет. '
                    'Билеты для посетителей младше 18 лет могут быть приобретены родителями или законными представителями.'
                )
            elif age > 120:
                raise forms.ValidationError('Пожалуйста, проверьте корректность даты рождения.')
        return birth_date

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Создаем или обновляем Visitor (взрослый пользователь)
            visitor, created = Visitor.objects.get_or_create(user=user)
            visitor.phone = self.cleaned_data.get('phone', '')
            visitor.birth_date = self.cleaned_data.get('birth_date')
            visitor.is_parent = True  # Отмечаем, что это родитель/законный представитель
            visitor.save()
            # Создаем Profile
            Profile.objects.get_or_create(user=user, defaults={"role": "visitor"})
        return user

class ChildForm(forms.ModelForm):
    """Форма для добавления ребенка"""
    
    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'first_name': 'Имя ребенка',
            'last_name': 'Фамилия ребенка',
            'birth_date': 'Дата рождения',
        }
        help_texts = {
            'birth_date': 'Дети до 18 лет получают льготный билет',
        }
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            from datetime import date
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age >= 18:
                raise forms.ValidationError('Ребенок должен быть младше 18 лет для льготного билета.')
            if age < 0:
                raise forms.ValidationError('Некорректная дата рождения.')
        return birth_date

class ExhibitionForm(forms.ModelForm):
    class Meta:
        model = Exhibition
        fields = ["museum", "title", "description", "start_date", "end_date", "guides", "is_active"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text", "image"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "text": forms.Textarea(attrs={"rows": 5}),
        }


class TicketBookingForm(forms.Form):
    exhibition = forms.ModelChoiceField(queryset=Exhibition.objects.none(), label="Выставка")
    
    VISITOR_TYPE_CHOICES = [
        ('adult', 'Взрослый (18+)'),
        ('child', 'Ребенок/школьник (до 18 лет) - льготный билет'),
    ]
    visitor_type = forms.ChoiceField(choices=VISITOR_TYPE_CHOICES, label="Тип посетителя", initial='adult')
    
    # Множественный выбор детей
    children = forms.ModelMultipleChoiceField(
        queryset=Child.objects.none(),
        required=False,
        label="Выберите детей",
        help_text="Можно выбрать несколько детей (Ctrl + клик или Shift + клик)",
        widget=forms.SelectMultiple(attrs={'size': 5, 'class': 'form-control'})
    )
    
    quantity = forms.IntegerField(min_value=1, max_value=10, initial=1, label="Количество билетов")

    def __init__(self, *args, **kwargs):
        exhibitions = kwargs.pop("exhibitions", Exhibition.objects.none())
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        
        self.fields["exhibition"].queryset = exhibitions
        
        if user and user.is_authenticated and hasattr(user, 'visitor'):
            children = user.visitor.children.all()
            
            if children.exists():
                self.fields['children'].queryset = children
                self.fields['children'].widget.attrs.update({'size': min(6, children.count() + 1)})
            else:
                self.fields['children'].widget = forms.HiddenInput()
                self.fields['children'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        visitor_type = cleaned_data.get('visitor_type')
        children = cleaned_data.get('children')
        
        # Проверка: если выбран тип "ребенок", должны быть выбраны дети
        if visitor_type == 'child' and (not children or len(children) == 0):
            raise forms.ValidationError('Выберите хотя бы одного ребенка для льготного билета.')
        
        return cleaned_data
    
    
class VisitorProfileForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['phone', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }