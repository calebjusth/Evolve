# jobs/forms.py
from django import forms
from django.core.validators import FileExtensionValidator

class JobApplicationForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Full Name',
            'required': True
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'youremail@example.com',
            'required': True
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+251912345678',
            'required': True
        })
    )
    
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your complete address',
            'rows': 3,
            'required': True
        })
    )
    
    cover_letter = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tell us why you are interested in this position...',
            'rows': 5,
            'required': True
        })
    )
    
    resume = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx',
            'required': True
        })
    )
    
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Limit file size to 5MB
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 5MB.")
        return resume