from django import forms
from mptt.forms import TreeNodeChoiceField

from .models import CategoryModelMPTT, ProductModel


class ProductAdminForm(forms.ModelForm):
    """Custom Form for ProductModel MPTT"""

    category = TreeNodeChoiceField(queryset=CategoryModelMPTT.objects.all())

    class Meta:
        model = ProductModel
        fields = "__all__"


class FilterForm(forms.Form):
    min_price = forms.DecimalField(
        required=False, min_value=0, max_digits=10, decimal_places=2
    )
    max_price = forms.DecimalField(
        required=False, min_value=0, max_digits=10, decimal_places=2
    )
    in_stock = forms.BooleanField(required=False)
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ("price_asc", "Ціна: за зростанням"),
            ("price_desc", "Ціна: за спаданням"),
            ("name_asc", "Назва: А-Я"),
            ("name_desc", "Назва: Я-А"),
        ],
    )


class SearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=100)
