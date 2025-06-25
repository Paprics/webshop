# search_engines.py
from django.db.models import Q


class SearchSQLite:
    def __init__(self, data):
        self.data = data

    def search(self, qs):
        q = self.data.get("q")
        if not q:
            return qs

        words = q.split()
        query = Q()
        for word in words:
            query |= Q(title__icontains=word) | Q(description__icontains=word)

        return qs.filter(query)

    def filter(self, qs):

        min_price = self.data.get("min_price")
        max_price = self.data.get("max_price")
        in_stock = self.data.get("in_stock")
        sort_by = self.data.get("sort_by")

        if min_price:
            qs = qs.filter(price__gte=min_price)

        if max_price:
            qs = qs.filter(price__lte=max_price)

        if in_stock:
            qs = qs.filter(in_stock=True)  # This field needs to be added to the database table. (maybe:))

        if sort_by == "name":
            qs = qs.order_by("name")
        elif sort_by == "-name":
            qs = qs.order_by("-name")
        elif sort_by == "price":
            qs = qs.order_by("price")
        elif sort_by == "-price":
            qs = qs.order_by("-price")

        return qs


class SearchPostgres: ...
