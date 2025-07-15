from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, TemplateView

from common.forms import FeedbackForm
from common.models import Feedback
from store.models import CategoryModelMPTT, ProductModel

from . import tasks_celery as tasks


class CustomerDetailView(DetailView):
    model = get_user_model()
    template_name = "customer_datail.html"
    context_object_name = "customer"

    def get_object(self):
        return (
            get_user_model()
            .objects.select_related("profile")
            .get(pk=self.request.user.pk)
        )


class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = {"title": "Home Page | Домашня сторінка"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = CategoryModelMPTT.objects.filter(
            parent=None, is_active=True
        ).order_by("display_order")
        category_products = []
        for cat in categories:
            descendants = cat.get_descendants(include_self=True)
            products = ProductModel.objects.filter(
                category__in=descendants, is_active=True
            ).order_by("-id")[:3]
            category_products.append({"category": cat, "products": products})
        context["category_products"] = category_products
        return context


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
    extra_context = {
        "info": "Задачу зі створення категорій успішно розпочато. Це може зайняти кілька секунд."
    }

    def get(self, request, *args, **kwargs):
        try:
            tasks.create_categories.delay()
        except Exception:
            tasks.create_categories()
        return super().get(request, *args, **kwargs)


class CreateProductsView(TemplateView):
    template_name = "create.html"
    extra_context = {
        "info": "Задачу зі створення товарів успішно розпочато. Зачекайте, поки товари будуть згенеровані."
    }

    def get(self, request, *args, **kwargs):
        try:
            tasks.create_products.delay()
        except Exception:
            tasks.create_products()

        return super().get(request, *args, **kwargs)


class CreateAskrateView(TemplateView):
    template_name = "create.html"
    extra_context = {
        "info": "Задачу зі створення відгуків та запитань до товарів розпочато. Результати з’являться невдовзі."
    }

    def get(self, request, *args, **kwargs):
        try:
            tasks.create_askrate.delay()
        except Exception:
            tasks.create_askrate()

        return super().get(request, *args, **kwargs)
