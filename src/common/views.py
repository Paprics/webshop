from django.shortcuts import render  # noqa F401
from django.views.generic import DetailView, TemplateView

from common.models import Content


class IndexView(DetailView):
    model = Content
    template_name = "index.html"
    context_object_name = "content"
    extra_context = {"title": "Home Page | Домашня сторінка"}

    def get_object(self):
        return Content.objects.get(pk=1)


class Page404View(TemplateView):
    template_name = "page404.html"
    extra_context = {"title": "Page 404 | Сторінку не знайдено"}


class AboutView(DetailView):
    model = Content
    template_name = "about.html"
    context_object_name = "about"
    extra_context = {"title": "About | Про нас"}

    def get_object(self):
        return Content.objects.get(pk=1)


class ContactView(TemplateView):
    template_name = "contacts.html"
    extra_context = {"title": "Contacts | Наші контакти"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = Content.objects.filter(pk=2)
        return context


class FaqView(DetailView):
    model = Content
    template_name = "faq.html"
    context_object_name = "faq"
    extra_context = {"title": "FAQ | Запитання"}

    def get_object(self):
        return Content.objects.get(pk=3)
