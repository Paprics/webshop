from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "askrate"

urlpatterns = [
    path("create/", views.AskRateCreateView.as_view(), name="create"),
    path("", TemplateView.as_view(template_name="askratee.html")),
]
