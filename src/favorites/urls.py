from django.urls import path

from favorites import views

app_name = "favorites"

urlpatterns = [
    path("", views.FavoriteView.as_view(), name="favorite_list"),
    path("cabinet/", views.FavoriteView.as_view(template_name="favorite_list_cabinet.html"), name="favorite_list_cabinet"),
    path("favorite/<int:pk>/", views.FavoriteView.as_view(), name="add"),
]
