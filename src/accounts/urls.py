from django.urls import path
from django.views.generic import TemplateView

from . import views
from .password_reset_views import (CustomPasswordResetCompleteView,
                                   CustomPasswordResetConfirmView,
                                   CustomPasswordResetDoneView,
                                   CustomPasswordResetView)

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("delete_account/", views.DeleteAccountView.as_view(), name="delete_account"),
    path("change_password/", views.PassChangeView.as_view(), name="change_password"),
    path("update_customer/", views.UpdateCustomerView.as_view(), name="update_customer"),
    path("update_delyvery/", views.UpdateDelyAddressView.as_view(), name="update_delyvery"),
    # Активация аккаунта
    path("activate/<uidb64>/<token>/", views.ActivateAccountView.as_view(), name="activate_account"),
    path("activate/success/", TemplateView.as_view(template_name="activation_success.html"), name="activation_success"),
    path("activate/failed/", TemplateView.as_view(template_name="activation_failed.html"), name="activation_failed"),
    path("activate/info/", TemplateView.as_view(template_name="activation_massage.html"), name="activation_massage"),
    # Восстановление пароля
    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
