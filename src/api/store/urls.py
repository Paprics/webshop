from django.urls import path
from rest_framework.routers import DefaultRouter

from api.store import views
from api.store.views import ContentViewApiList

app_name = "api_store"

# for ViewSet(CRUD) class
router = DefaultRouter()
router.register(r"categories", views.CategoriesViewApi, basename="categories")
router.register(r"categories_nested", views.CategoriesMPTTViewApi, basename="categories_nested")

urlpatterns = router.urls + [
    path("test/", views.test_api),  # обычная функция или APIView
    path("content/<int:pk>/", views.ContentViewApiRetrieve.as_view(), name="content-retrieve"),
    path("content/list/", ContentViewApiList.as_view(), name="content-list"),
]
