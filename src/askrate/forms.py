from django import forms

from askrate.models import AskRateModel


class AskRateForms(forms.ModelForm):
    class Meta:
        model = AskRateModel
        fields = ["rating", "text", "type", "product"]
        labels = {
            "text": "Ваш відгук або питання",
            "rating": "Оцінка",
        }
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4, "placeholder": "Напишіть тут свій відгук або питання"}),
            "rating": forms.RadioSelect(),
        }
