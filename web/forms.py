from django import forms
from .models import Birthplace

# Create your Forms here.

class ContactForm(forms.Form):
    
    gender_choices = [
        ('', ''),
        ('F', 'female'),
        ('M', 'male'),
        ('Others', 'Undefined gender')
    ]
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs= {
                'class': 'form-control',
                'placeholder': 'Subject',
                'title': 'Subject'
            }
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Test message ...',
                'title': 'Message',
                'aria-label': 'With textarea'
            }
        )
    )
    sender = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'title': 'Email'
            }
        )
    )
    cc_myself = forms.BooleanField(required=False)
    city_select = forms.ChoiceField(
        choices=gender_choices,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )
    ethnicity = forms.RadioSelect(
            attrs={
                'class': 'form-check-input'
            },choices=[
                ('Amerindian', 'amerindian'),
                ('Asian', 'asian'),
                ('Black', 'black'),
                ('Caboclo(a)', 'caboclo'),
                ('Cafuzo(a)', 'cafuzo'),
                ('Caucasian', 'caucasian'),
                ('Mulato(a)', 'mulato')
            ]
        )