from django import forms
from .models import Review, Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['last_name', 'first_name', 'bio']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']

