from django.urls import path

from favorites import views

app_name = "favorites"

urlpatterns = [
    path("", views.FavoriteView.as_view(), name="list"),
    path("favorite/<int:pk>", views.FavoriteView.as_view(), name="add"),
]
