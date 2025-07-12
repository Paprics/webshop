from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = "reset/password_reset_form.html"
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "reset/password_reset_done.html"


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"
