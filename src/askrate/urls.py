from django.urls import path
from django.views.generic import TemplateView

app_name = "askrate"

urlpatterns = [
    path('', TemplateView.as_view(template_name='askratee.html'))
]