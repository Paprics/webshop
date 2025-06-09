from django import forms
from mptt.forms import TreeNodeChoiceField

from .models import CategoryModelMPTT, ProductModel


class ProductAdminForm(forms.ModelForm):
    """Custom Form for ProductModel MPTT"""

    category = TreeNodeChoiceField(queryset=CategoryModelMPTT.objects.all())

    class Meta:
        model = ProductModel
        fields = "__all__"
