from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Exhibition, Review


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


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
    exhibition = forms.ModelChoiceField(queryset=Exhibition.objects.none())

    def __init__(self, *args, **kwargs):
        exhibitions = kwargs.pop("exhibitions", Exhibition.objects.none())
        super().__init__(*args, **kwargs)
        self.fields["exhibition"].queryset = exhibitions
