from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'phone', 'company', 'inquiry_type', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control cyber-input', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control cyber-input', 'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control cyber-input', 'placeholder': '+234 xxx xxx xxxx'}),
            'company': forms.TextInput(attrs={'class': 'form-control cyber-input', 'placeholder': 'Company / Organization'}),
            'inquiry_type': forms.Select(attrs={'class': 'form-select cyber-input'}),
            'subject': forms.TextInput(attrs={'class': 'form-control cyber-input', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control cyber-input', 'rows': 5, 'placeholder': 'Your message...'}),
        }
