from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomLoginForm(AuthenticationForm):
    """Custom login form - simplified since user type is set during registration"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style the form fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    PROFILE_TYPE_CHOICES = [
        ('buyer', 'Buyer Only - Shop for fashion products'),
        ('seller', 'Seller Only - Sell fashion products'),
        ('both', 'Both - Buy and sell fashion products'),
    ]
    
    user_type = forms.ChoiceField(
        choices=PROFILE_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-radio'}),
        required=True,
        label="How do you want to create your profile?",
        help_text="Choose the type of profile that best fits your needs"
    )
    
    # Seller-specific fields (optional)
    business_name = forms.CharField(
        max_length=100, 
        required=False,
        help_text="Required for seller and both profiles"
    )
    business_description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text="Describe your business (optional)"
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ != 'RadioSelect':
                field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            
            # Make business_name required for seller types
            if field_name == 'business_name':
                field.widget.attrs['placeholder'] = 'Enter your business name'
            elif field_name == 'business_description':
                field.widget.attrs['placeholder'] = 'Tell us about your business...'
    
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        business_name = cleaned_data.get('business_name')
        
        # Validate business_name is required for seller types
        if user_type in ['seller', 'both'] and not business_name:
            raise forms.ValidationError("Business name is required for seller profiles.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        user.business_name = self.cleaned_data.get('business_name', '')
        user.business_description = self.cleaned_data.get('business_description', '')
        
        # Auto-verify sellers for now (in production, this would be manual)
        if user.user_type in ['seller', 'both']:
            user.is_verified_seller = True
        
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'height_cm', 'weight_kg', 
            'body_type', 'gender', 'chest_cm', 'waist_cm', 'hips_cm'
        ]
        widgets = {
            'height_cm': forms.NumberInput(attrs={'placeholder': 'Height in cm'}),
            'weight_kg': forms.NumberInput(attrs={'placeholder': 'Weight in kg'}),
            'chest_cm': forms.NumberInput(attrs={'placeholder': 'Chest measurement in cm'}),
            'waist_cm': forms.NumberInput(attrs={'placeholder': 'Waist measurement in cm'}),
            'hips_cm': forms.NumberInput(attrs={'placeholder': 'Hips measurement in cm'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
