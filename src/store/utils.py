from faker import Faker

from store.models import CategoryModelMPTT, ProductModel


def create_categories():
    clothes = CategoryModelMPTT.objects.create(category_name="Одяг", display_order=1)
    shoes = CategoryModelMPTT.objects.create(category_name="Взуття", display_order=2)
    backpacks_and_bags = CategoryModelMPTT.objects.create(category_name="Рюкзаки та сумки", display_order=3)
    accessories = CategoryModelMPTT.objects.create(category_name="Аксесуари", display_order=4)

    CategoryModelMPTT.objects.create(category_name="Черевики", display_order=1, parent=shoes)
    CategoryModelMPTT.objects.create(category_name="Кросівки", display_order=2, parent=shoes)
    CategoryModelMPTT.objects.create(category_name="Сандалі", display_order=3, parent=shoes)
    CategoryModelMPTT.objects.create(category_name="Ботинки", display_order=4, parent=shoes)

    CategoryModelMPTT.objects.create(category_name="Рюкзаки", display_order=1, parent=backpacks_and_bags)
    CategoryModelMPTT.objects.create(category_name="Сумки", display_order=2, parent=backpacks_and_bags)
    CategoryModelMPTT.objects.create(category_name="Сумки через плече", display_order=3, parent=backpacks_and_bags)

    CategoryModelMPTT.objects.create(category_name="Рубашки", display_order=1, parent=accessories)
    CategoryModelMPTT.objects.create(category_name="Шапки", display_order=2, parent=accessories)
    CategoryModelMPTT.objects.create(category_name="Ремені", display_order=3, parent=accessories)
    CategoryModelMPTT.objects.create(category_name="Шкарпетки", display_order=4, parent=accessories)

    CategoryModelMPTT.objects.create(category_name="Куртки", display_order=1, parent=clothes)
    CategoryModelMPTT.objects.create(category_name="Штани", display_order=2, parent=clothes)
    CategoryModelMPTT.objects.create(category_name="Футболки", display_order=3, parent=clothes)
    CategoryModelMPTT.objects.create(category_name="Светри", display_order=4, parent=clothes)
    CategoryModelMPTT.objects.create(category_name="Термобілизна", display_order=5, parent=clothes)


def create_products():
    faker = Faker("uk_UA")
    QUNTYTI_PRODUCT = 40
    categories = CategoryModelMPTT.objects.filter(parent__isnull=False)

    products_to_create = []
    for category in categories:
        for _ in range(QUNTYTI_PRODUCT):
            product = ProductModel(
                title=faker.sentence(nb_words=2).rstrip(".").capitalize(),
                slug=faker.slug()[:100],
                article=faker.unique.bothify(text="??####"),
                price=round(faker.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
                description=faker.text(max_nb_chars=500),
                quantity=faker.random_int(min=1, max=20),
                category=category,
                is_active=True,
            )
            products_to_create.append(product)

    ProductModel.objects.bulk_create(products_to_create)
