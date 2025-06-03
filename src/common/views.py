from django.shortcuts import render  # noqa F401
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = {"title": "Home Page | Домашня сторінка"}