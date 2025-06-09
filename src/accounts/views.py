from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy



class LoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('common:index')



class LogoutView(LogoutView):
    next_page = 'login'