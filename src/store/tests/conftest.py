import pytest
from django.contrib.auth import get_user_model
from faker import Faker

from store.models import CategoryModelMPTT, ProductModel


@pytest.fixture
def create_categories():
    names = ["Чоловіче", "Жіноче", "Дитяче", "Аксесуари", "Інше"]
    categories = []
    for name in names:
        category = CategoryModelMPTT(category_name=name)
        category.full_clean()
        category.save()
        categories.append(category)
    return categories


@pytest.fixture
def create_product(create_categories):
    fake = Faker()
    title = fake.word()
    article = fake.bothify(text="???-#####")
    price = fake.pydecimal(left_digits=4, right_digits=2, positive=True)
    description = fake.text(max_nb_chars=950)
    quantity = fake.random_int(max=100)

    # ForeignKey expects a CategoryModel
    category = create_categories[0]

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

    return product


@pytest.fixture
def create_customer():
    Customer = get_user_model()
    customer = Customer(
        phone_number="+380991234567",
        email="example@qwe.com",
    )
    customer.set_password("123qwezxc")
    customer.save()

    return customer
