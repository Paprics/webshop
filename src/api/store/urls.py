from django.urls import path
from rest_framework.routers import DefaultRouter
from api.store import views

app_name = "api_store"

# Settings for setView (3 rows)
router = DefaultRouter()
router.register(r'categories', views.CategoriesViewApi, basename='categories')
urlpatterns = router.urls

urlpatterns = router.urls + [
    path('test/', views.test_api),
]


