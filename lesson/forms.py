from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import LearningProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class LearningProfileForm(forms.ModelForm):
    class Meta:
        model = LearningProfile
        fields = [
            'learning_style', 'difficulty_level', 'concentration_level',
            'subjects_studying', 'academic_goals', 'study_challenges',
            'available_hours_per_day', 'preferred_study_times'
        ]
        widgets = {
            'subjects_studying': forms.TextInput(attrs={'placeholder': 'e.g., Mathematics, English, Biology, History'}),
            'academic_goals': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What are your main academic goals?'}),
            'study_challenges': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What challenges do you face when studying?'}),
        }