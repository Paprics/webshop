import pytest

from store.models import CategoryModelMPTT


class TestProduct:

    @pytest.mark.parametrize(
        "category_name",
        [
            "Чоловіче",
            "Жіноче",
            "Дитяче",
            "Аксесуари",
            "Інше",
        ],
    )
    @pytest.mark.django_db
    def test_create_category(self, category_name):
        CategoryModelMPTT.objects.create(category_name=category_name)
        assert CategoryModelMPTT.objects.filter(category_name=category_name).exists()
