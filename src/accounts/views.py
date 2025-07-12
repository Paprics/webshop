from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import DeleteView, UpdateView, RedirectView, CreateView

from accounts.forms import MemberCreationForm
from accounts.models import ProfileCustomer
from .utils.utils import TokenGenerator, send_registration_mail


class UpdateDelyAddressView(UpdateView):
    model = ProfileCustomer
    fields = ("delivery_address", "additional_contacts")
    template_name = "update_dely_address.html"
    success_url = reverse_lazy("common:customer_detail")

    def get_object(self):
        profile, created = ProfileCustomer.objects.get_or_create(customer=self.request.user)
        return profile


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


class LoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("common:index")


class LogoutView(LogoutView):
    next_page = reverse_lazy("common:index")



class RegistrationView(CreateView):
    model = get_user_model()
    form_class = MemberCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("accounts:activation_massage")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()

        send_registration_mail(customer=self.object, request=self.request)

        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("common:index"))
        return super().dispatch(request, *args, **kwargs)


class ActivateAccountView(RedirectView):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            pk = int(urlsafe_base64_decode(uidb64).decode())
            current_user = get_user_model().objects.get(pk=pk)

        except (get_user_model().DoesNotExist, ValueError):
            return redirect("accounts:activation_failed")

        if current_user.is_active:
            return redirect("accounts:activation_failed")

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()

            login(request, current_user)

            return redirect("accounts:activation_success")

        return redirect("accounts:activation_failed")
