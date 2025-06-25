# search_engines.py
from django.contrib.postgres.search import SearchVector
from django.db.models import Q


class BaseSearchEngine:
    def __init__(self, data):
        self.data = data

    def filter(self, qs, cleaned_data):

        min_price = cleaned_data.get("min_price")
        max_price = cleaned_data.get("max_price")
        in_stock = cleaned_data.get("in_stock")
        sort_by = cleaned_data.get("sort_by")

        if min_price is not None:
            qs = qs.filter(price__gte=min_price)

        if max_price is not None:
            qs = qs.filter(price__lte=max_price)

        if in_stock:
            qs = qs.filter(quantity__gt=0, is_active=True)

        sort_map = {
            "price_asc": "price",
            "price_desc": "-price",
            "name_asc": "title",
            "name_desc": "-title",
        }

        if sort_by in sort_map:
            qs = qs.order_by(sort_map[sort_by])

        return qs


class SQLiteSearchEngine(BaseSearchEngine):

    def search(self, qs):
        q = self.data.get("q")
        if not q:
            return qs

        words = q.split()
        query = Q()
        for word in words:
            query |= Q(title__icontains=word) | Q(description__icontains=word)

        return qs.filter(query)


class PostgresSearchEngine(BaseSearchEngine):

    def search(self, qs):
        q = self.data.get("q")
        if not q:
            return qs
        return qs.annotate(search=SearchVector("title", "description")).filter(search=q)
