# movies/forms.py
from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        widgets = {
            'value': forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)])
        }


