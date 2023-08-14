# certificates/forms.py

from django import forms
from .models import Certificate, Customization


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['title', 'recipient_name', 'issue_date']

class CustomizationForm(forms.ModelForm):
    class Meta:
        model = Customization
        fields = ['font', 'color', 'layout']
