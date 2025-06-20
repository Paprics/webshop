from django.urls import path
from django.views.generic import TemplateView

from common import views

app_name = "common"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contacts/", views.ContactView.as_view(), name="contacts"),
    path("fqa/", views.FaqView.as_view(), name="faq"),
    path("page404/", views.Page404View.as_view(), name="page404"),
    path("feedback/", views.Feedback.as_view(), name="feedback"),
    path("settings/", TemplateView.as_view(template_name="settings.html"), name="settings"),
]
