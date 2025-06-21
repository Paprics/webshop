from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, FormView, UpdateView

from accounts.models import ProfileCustomer
from accounts.rorms import MemberCreationForm


class UpdateDelyAddressView(UpdateView):
    model = ProfileCustomer
    fields = ("delivery_address", "additional_contacts")
    template_name = "update_dely_address.html"
    success_url = reverse_lazy("common:customer_detail")

    def get_object(self):
        return self.request.user.profile


class UpdateCustomerView(UpdateView):
    model = get_user_model()
    template_name = "update_customer.html"
    fields = ("first_name", "last_name", "phone_number", "email")
    success_url = reverse_lazy("common:customer_detail")

    def get_object(self):
        return self.request.user


class PassChangeView(PasswordChangeView):
    template_name = "chenge_password.html"
    success_url = reverse_lazy("accounts:change_password")
    form_class = PasswordChangeForm


class DeleteAccountView(DeleteView):
    model = get_user_model()
    template_name = "delete_account.html"
    success_url = reverse_lazy("common:index")

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = MemberCreationForm
    success_url = reverse_lazy("common:index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("common:index"))
        return super().dispatch(request, *args, **kwargs)


class LoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("common:index")


class LogoutView(LogoutView):
    next_page = reverse_lazy("common:index")
