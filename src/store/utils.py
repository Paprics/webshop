from faker import Faker

from store.models import CategoryModelMPTT, ProductModel


def create_categories():
    def make_slug(name, idx):
        return f"cat_{idx}"

    clothes = CategoryModelMPTT.objects.create(category_name="Одяг", display_order=1, slug=make_slug("Одяг", 1))
    shoes = CategoryModelMPTT.objects.create(category_name="Взуття", display_order=2, slug=make_slug("Взуття", 2))
    backpacks_and_bags = CategoryModelMPTT.objects.create(
        category_name="Рюкзаки та сумки", display_order=3, slug=make_slug("Рюкзаки та сумки", 3)
    )
    accessories = CategoryModelMPTT.objects.create(
        category_name="Аксесуари", display_order=4, slug=make_slug("Аксесуари", 4)
    )

    CategoryModelMPTT.objects.create(
        category_name="Черевики", display_order=1, parent=shoes, slug=make_slug("Черевики", 5)
    )
    CategoryModelMPTT.objects.create(
        category_name="Кросівки", display_order=2, parent=shoes, slug=make_slug("Кросівки", 6)
    )
    CategoryModelMPTT.objects.create(
        category_name="Сандалі", display_order=3, parent=shoes, slug=make_slug("Сандалі", 7)
    )
    CategoryModelMPTT.objects.create(
        category_name="Ботинки", display_order=4, parent=shoes, slug=make_slug("Ботинки", 8)
    )

    CategoryModelMPTT.objects.create(
        category_name="Рюкзаки", display_order=1, parent=backpacks_and_bags, slug=make_slug("Рюкзаки", 9)
    )
    CategoryModelMPTT.objects.create(
        category_name="Сумки", display_order=2, parent=backpacks_and_bags, slug=make_slug("Сумки", 10)
    )
    CategoryModelMPTT.objects.create(
        category_name="Сумки через плече",
        display_order=3,
        parent=backpacks_and_bags,
        slug=make_slug("Сумки через плече", 11),
    )

    CategoryModelMPTT.objects.create(
        category_name="Рубашки", display_order=1, parent=accessories, slug=make_slug("Рубашки", 12)
    )
    CategoryModelMPTT.objects.create(
        category_name="Шапки", display_order=2, parent=accessories, slug=make_slug("Шапки", 13)
    )
    CategoryModelMPTT.objects.create(
        category_name="Ремені", display_order=3, parent=accessories, slug=make_slug("Ремені", 14)
    )
    CategoryModelMPTT.objects.create(
        category_name="Шкарпетки", display_order=4, parent=accessories, slug=make_slug("Шкарпетки", 15)
    )

    CategoryModelMPTT.objects.create(
        category_name="Куртки", display_order=1, parent=clothes, slug=make_slug("Куртки", 16)
    )
    CategoryModelMPTT.objects.create(
        category_name="Штани", display_order=2, parent=clothes, slug=make_slug("Штани", 17)
    )
    CategoryModelMPTT.objects.create(
        category_name="Футболки", display_order=3, parent=clothes, slug=make_slug("Футболки", 18)
    )
    CategoryModelMPTT.objects.create(
        category_name="Светри", display_order=4, parent=clothes, slug=make_slug("Светри", 19)
    )
    CategoryModelMPTT.objects.create(
        category_name="Термобілизна", display_order=5, parent=clothes, slug=make_slug("Термобілизна", 20)
    )


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
