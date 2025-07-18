from django.urls import path
from django.views.generic import TemplateView

from common import views

app_name = "common"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path(
        "contacts/",
        TemplateView.as_view(template_name="contacts.html"),
        name="contacts",
    ),
    path("fqa/", TemplateView.as_view(template_name="faq.html"), name="faq"),
    path("page404/", TemplateView.as_view(template_name="404.html"), name="page404"),
    path("feedback/", views.FeedbackCreateView.as_view(), name="feedback"),
    path(
        "success_feedback/",
        TemplateView.as_view(template_name="success_feedback.html"),
        name="success_feedback",
    ),
    path("customer_detail/", views.CustomerDetailView.as_view(), name="customer_detail"),
    path("create_category/", views.CreateCategoryView.as_view(), name="create_category"),
    path("create_products/", views.CreateProductsView.as_view(), name="create_products"),
    path("create_askrate/", views.CreateAskrateView.as_view(), name="create_askrate"),
    path(
        "success_order/",
        TemplateView.as_view(template_name="success_order.html"),
        name="success_order",
    ),
]
