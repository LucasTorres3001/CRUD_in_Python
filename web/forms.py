from django import forms

# Create your Forms here.

class ContactForm(forms.Form):
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