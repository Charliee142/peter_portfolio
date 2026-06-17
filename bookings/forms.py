from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['slot', 'full_name', 'email', 'phone', 'company', 'consultation_type', 'description']
        widgets = {
            'slot': forms.Select(attrs={'class': 'form-select cyber-input'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control cyber-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control cyber-input', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control cyber-input'}),
            'company': forms.TextInput(attrs={'class': 'form-control cyber-input'}),
            'consultation_type': forms.Select(attrs={'class': 'form-select cyber-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control cyber-input', 'rows': 4}),
        }
