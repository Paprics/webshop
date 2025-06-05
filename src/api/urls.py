from django.urls import include, path

app_name = "api_base"

urlpatterns = [
    path("store/", include("api.store.urls")),
]
