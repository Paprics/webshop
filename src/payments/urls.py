from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "payments"
urlpatterns = [
    path("", views.PayOrderView.as_view(), name="pay"),
    path("success/", TemplateView.as_view(template_name="success.html"), name="success"),
    path("cancel/", TemplateView.as_view(template_name="cancel.html"), name="cancel"),
]
