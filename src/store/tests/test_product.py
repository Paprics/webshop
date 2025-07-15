import pytest
from django.core.exceptions import ValidationError
from faker import Faker

from store.models import ProductModel
from store.tests.conftest import create_categories  # noqa F811


class TestProduct:

    @pytest.mark.django_db
    def test_create_product(self, create_categories):  # noqa F811
        fake = Faker()
        title = fake.word()
        article = fake.bothify(text="???-#####")
        price = fake.pydecimal(left_digits=4, right_digits=2, positive=True)
        description = fake.text(max_nb_chars=950)
        quantity = fake.random_int(max=100)

        category = create_categories[0]  # ForeignKey expects a CategoryModel instance (not a string❗)

        product = ProductModel(
            title=title,
            article=article,
            price=price,
            description=description,
            quantity=quantity,
            category=category,
        )

        product.full_clean()
        product.save()

        qs = ProductModel.objects.get(pk=product.pk)
        assert qs.title == title
        assert qs.article == article
        assert qs.price == price
        assert qs.description == description
        assert qs.quantity == quantity
        assert qs.category.category_name == category.category_name

    @pytest.mark.xfail
    @pytest.mark.django_db
    def test_wrong_create_product(self, create_categories):  # noqa F811

        fake = Faker()
        title = fake.text(max_nb_chars=120)
        article = fake.bothify(text="???-#####" * 10)
        price = fake.pydecimal(left_digits=4, right_digits=2, positive=True)

        # NOTE: MaxLength validation on TextField is enforced only at the database level, not by Django validators.
        description = fake.text(max_nb_chars=1001)  # full_clean() only triggers defined validators.

        quantity = fake.random_int(max=100)

        category = create_categories[3]

        product = ProductModel(
            title=title,
            article=article,
            price=price,
            description=description,
            quantity=quantity,
            category=category,
        )

        with pytest.raises(ValidationError) as error_info:
            product.full_clean()
            product.save()

        # TODO: MaxLength validation
        assert "title" in error_info.value.error_dict
        assert "article" in error_info.value.error_dict
        assert "description" in error_info.value.error_dict
