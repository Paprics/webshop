from django.contrib.auth import get_user_model
from django.views.generic import DetailView, FormView

from common.forms import FeedbackForm
from common.models import Content


class CustomerDetailView(DetailView):
    model = get_user_model()
    template_name = "customer_datail.html"
    context_object_name = "customer"

    def get_object(self):
        return get_user_model().objects.select_related("profile").get(pk=self.request.user.pk)


class IndexView(DetailView):
    model = Content
    template_name = "index.html"
    context_object_name = "content"
    extra_context = {"title": "Home Page | Домашня сторінка"}

    def get_object(self):
        return Content.objects.filter(pk=1)


class Feedback(FormView):
    form_class = FeedbackForm
    http_method_names = ["get", "post"]
    template_name = "feedback.html"
    success_url = "/"

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        else:
            form.instance.user = None
        form.save()
        return super().form_valid(form)
