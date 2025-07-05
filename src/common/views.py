from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, TemplateView

from common.forms import FeedbackForm
from common.models import Content, Feedback

from . import tasks_celery as tasks


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


class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = "feedback.html"
    success_url = reverse_lazy("common:success_feedback")

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super().form_valid(form)


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


class CreateCategoryView(TemplateView):
    template_name = "create.html"

    def get(self, request, *args, **kwargs):
        tasks.create_categories.delay()
        return super().get(request, *args, **kwargs)


class CreateProductsView(TemplateView):
    template_name = "create.html"

    def get(self, request, *args, **kwargs):
        tasks.create_products.delay()
        return super().get(request, *args, **kwargs)
