from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from .models import MovieRequest, UserProfile


class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ""
        return mark_safe(
            "".join(
                [
                    f'<div class="alert alert-danger" role="alert">{e}</div>'
                    for e in self
                ]
            )
        )


class CustomUserCreationForm(UserCreationForm):
    # Add location fields to signup form
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"})
    )
    country = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Country (optional)"})
    )
    city = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "City (optional)"})
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Add Bootstrap classes to ALL fields
        for field_name, field in self.fields.items():
            if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
                field.widget.attrs['class'] = 'form-control'
            field.help_text = None  # Remove help text
    
    class Meta:
        model = UserCreationForm.Meta.model
        fields = ["username", "email", "password1", "password2", "country", "city"]
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Save location data to user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.country = self.cleaned_data.get('country')
            profile.city = self.cleaned_data.get('city')
            profile.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ["username", "password1", "password2", "email", "country", "city"]:
            self.fields[fieldname].help_text = None
            if fieldname not in ["email", "country", "city"]:  # Already have class from above
                self.fields[fieldname].widget.attrs.update({"class": "form-control"})
    
    class Meta:
        model = UserCreationForm.Meta.model
        fields = ["username", "email", "password1", "password2", "country", "city"]
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Save location data to user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.country = self.cleaned_data.get('country')
            profile.city = self.cleaned_data.get('city')
            profile.save()
        return user


class MovieRequestForm(forms.ModelForm):
    class Meta:
        model = MovieRequest
        fields = ["movie_name", "reason"]
        widgets = {
            'movie_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie title'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Why do you want this movie?', 'rows': 3}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['country', 'state', 'city', 'zip_code']
        widgets = {
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., United States'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., California'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Los Angeles'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 90210'}),
        }
