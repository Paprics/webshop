from django.urls import path
from src.common import views

app_name = 'common'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]