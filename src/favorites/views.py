from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from favorites.models import FavoriteModel


class FavoriteView(LoginRequiredMixin, View):

    template_name = "favorites_list.html"
    # template_name = "favorite_list_cabinet.html"

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        action = request.POST.get("action")

        if action == "add":
            FavoriteModel.objects.get_or_create(customer=request.user, product_id=product_id)

        elif action == "remove":
            favorite = get_object_or_404(FavoriteModel, customer=request.user, product_id=product_id)
            favorite.delete()

        return redirect(request.META.get("HTTP_REFERER", "/"))

    def get(self, request, *args, **kwargs):
        favorites = FavoriteModel.objects.filter(customer=request.user)
        context = {"favorites": favorites}

        return render(request, self.template_name, context)


class FavoriteListView(ListView):
    template_name = "favorites_list.html"
