import pytest

from store.models import CategoryModel


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
        CategoryModel.objects.create(category_name=category_name)
        assert CategoryModel.objects.filter(category_name=category_name).exists()
