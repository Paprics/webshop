from django import forms

from common.models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["title", "message", "email", "phone_number"]
