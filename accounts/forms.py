from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from .models import MovieRequest


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
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({"class": "form-control"})


class MovieRequestForm(forms.ModelForm):
    class Meta:
        model = MovieRequest
        fields = ["movie_name", "reason"]
