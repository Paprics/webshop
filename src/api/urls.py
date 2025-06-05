from django.urls import path, include

app_name = 'api_base'

urlpatterns = [
    path('store/', include('api.store.urls')),
]