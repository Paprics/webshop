from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("delete_account/", views.DeleteAccountView.as_view(), name="delete_account"),
    path("change_password/", views.PassChangeView.as_view(), name="change_password"),
    path("update_customer/", views.UpdateCustomerView.as_view(), name="update_customer"),
    path("update_delyvery/", views.UpdateDelyAddressView.as_view(), name="update_delyvery"),
]
