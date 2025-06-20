from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, DeleteView

from accounts.rorms import MemberCreationForm
class DeleteAccountView(DeleteView):
    model = get_user_model()
    template_name = 'delete_account.html'
    success_url = reverse_lazy('common:index')

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
