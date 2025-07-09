import pytest
from faker import Faker

from store.models import CommentModel
from store.tests.conftest import create_customer, create_product  # noqa F401


class TestComment:

    @pytest.mark.django_db
    def test_create_comment(self, create_product, create_customer):  # noqa F811

        fake = Faker()
        text = fake.text(max_nb_chars=200)

        comment = CommentModel(
            customer=create_customer,
            product=create_product,
            text=text,
        )

        comment.full_clean()
        comment.save()

        qs = CommentModel.objects.get(pk=comment.pk)
        assert qs.customer
        assert qs.product
        assert qs.text == text
        assert qs.added_at is not None
        assert qs.is_active == True  # noqa F712
