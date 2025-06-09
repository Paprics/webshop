from mptt.forms import TreeNodeChoiceField
from django import forms
from .models import ProductModel, CategoryModelMPTT

class ProductAdminForm(forms.ModelForm):
    """Custom Form for ProductModel MPTT"""
    category = TreeNodeChoiceField(queryset=CategoryModelMPTT.objects.all())

    class Meta:
        model = ProductModel
        fields = "__all__"