from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'term-input',
        'placeholder': 'echo "Name"'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'term-input',
        'placeholder': 'echo "Email"'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'term-input',
        'placeholder': 'cat << EOF...',
        'rows': 4
    }))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
