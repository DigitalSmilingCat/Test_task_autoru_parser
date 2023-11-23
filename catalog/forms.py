from django import forms
from .models import *


class BrandSelectionForm(forms.Form):
    name = forms.ModelChoiceField(label='Brand name', queryset=CarBrand.objects.all())
