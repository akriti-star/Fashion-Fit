from django import forms
from .models import Outfit
from products.models import Product


class OutfitForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = Outfit
        fields = ['name', 'is_public', 'products']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter outfit name'}),
            'is_public': forms.CheckboxInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'


class OutfitBuilderForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Enter outfit name',
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
    }))
    is_public = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add product fields dynamically
        categories = ['top', 'bottom', 'dress', 'outerwear', 'shoes', 'accessories']
        for category in categories:
            products = Product.objects.filter(category=category, is_active=True)
            if products.exists():
                self.fields[f'{category}_products'] = forms.ModelMultipleChoiceField(
                    queryset=products,
                    widget=forms.CheckboxSelectMultiple,
                    required=False,
                    label=f'{category.title()} Items'
                )
