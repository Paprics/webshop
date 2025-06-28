from django.shortcuts import render
from django.views.generic import CreateView

from askrate.models import AskRateModel
from askrate.forms import AskRateForms


class AskRateCreateView(CreateView):
    model = AskRateModel
    form_class = AskRateForms

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')

    def form_valid(self, form):
        form.instance.customer = self.request.user if self.request.user.is_authenticated else None
        return super().form_valid(form)


