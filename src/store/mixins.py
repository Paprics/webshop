# mixins.py
from django.db.models import Exists, OuterRef

from favorites.models import FavoriteModel
from store.forms import FilterForm, SearchForm

from . import search_engines


class SearchFilterMixin:

    search_form_class = SearchForm
    filter_form_class = FilterForm
    search_engine_class = None

    def get_search_form(self):
        return self.search_form_class(self.request.GET)

    def get_filter_form(self):
        return self.filter_form_class(self.request.GET)

    def get_cleaned_data(self):
        """Объединяет cleaned_data из search и filter форм"""
        search_form = self.get_search_form()
        filter_form = self.get_filter_form()

        self._search_form = search_form
        self._filter_form = filter_form

        cleaned_data = {}

        if search_form.is_valid():
            cleaned_data.update(search_form.cleaned_data)

        if filter_form.is_valid():
            cleaned_data.update(filter_form.cleaned_data)

        return cleaned_data

    def get_search_engine(self, data):
        if self.search_engine_class is None:
            return search_engines.SQLiteSearchEngine(data)
        return self.search_engine_class(data)

    def get_queryset(self):
        qs = super().get_queryset()

        data = self.get_cleaned_data()
        engine = self.get_search_engine(data)

        qs = engine.search(qs)
        qs = engine.filter(qs, data)

        return qs

class FavoriteAnnotateMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            return qs.annotate(
                is_favorite=Exists(
                    FavoriteModel.objects.filter(
                        product=OuterRef('id'),
                        customer=self.request.user
                    )
                )
            )
        return qs