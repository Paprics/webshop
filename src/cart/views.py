from django.views.generic import TemplateView


class CartDetailView(TemplateView):
    template_name = 'cart_detail.html'
    # extra_context = {'s'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_menu'] = False
        return context