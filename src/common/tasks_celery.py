from time import sleep

from celery import shared_task
from faker import Faker

from store.models import CategoryModelMPTT, ProductModel


@shared_task
def create_categories():
    sleep(10)

    def make_slug(name, idx):
        return f"cat_{idx}"

    clothes, _ = CategoryModelMPTT.objects.get_or_create(
        category_name="Одяг",
        parent=None,
        defaults={"display_order": 1, "slug": make_slug("Одяг", 1)},
    )
    shoes, _ = CategoryModelMPTT.objects.get_or_create(
        category_name="Взуття",
        parent=None,
        defaults={"display_order": 2, "slug": make_slug("Взуття", 2)},
    )
    backpacks_and_bags, _ = CategoryModelMPTT.objects.get_or_create(
        category_name="Рюкзаки та сумки",
        parent=None,
        defaults={"display_order": 3, "slug": make_slug("Рюкзаки та сумки", 3)},
    )
    accessories, _ = CategoryModelMPTT.objects.get_or_create(
        category_name="Аксесуари",
        parent=None,
        defaults={"display_order": 4, "slug": make_slug("Аксесуари", 4)},
    )

    CategoryModelMPTT.objects.get_or_create(
        category_name="Черевики",
        parent=shoes,
        defaults={"display_order": 1, "slug": make_slug("Черевики", 5)},
    )
    CategoryModelMPTT.objects.get_or_create(
        category_name="Кросівки",
        parent=shoes,
        defaults={"display_order": 2, "slug": make_slug("Кросівки", 6)},
    )
    CategoryModelMPTT.objects.get_or_create(
        category_name="Сандалі",
        parent=shoes,
        defaults={"display_order": 3, "slug": make_slug("Сандалі", 7)},
    )
    CategoryModelMPTT.objects.get_or_create(
        category_name="Ботинки",
        parent=shoes,
        defaults={"display_order": 4, "slug": make_slug("Ботинки", 8)},
    )

    CategoryModelMPTT.objects.get_or_create(
        category_name="Рюкзаки",
        parent=backpacks_and_bags,
        defaults={"display_order": 1, "slug": make_slug("Рюкзаки", 9)},
    )
    CategoryModelMPTT.objects.get_or_create(
        category_name="Сумки",
        parent=backpacks_and_bags,
        defaults={"display_order": 2, "slug": make_slug("Сумки", 10)},
    )
    CategoryModelMPTT.objects.get_or_create(
        category_name="Сумки через плече",
        parent=backpacks_and_bags,
        defaults={"display_order": 3, "slug": make_slug("Сумки через плече", 11)},
    )

    CategoryModelMPTT.objects.get_or_create(
        category_name="Рубашки",
        parent=accessories,
        defaults={"display_order": 1, "slug": make_slug("Рубашки", 12)},
    )
    CategoryModelMPTT.objects.get_or_create(
        category_name="Шапки",
        parent=accessories,
        defaults={"display_order": 2, "slug": make_slug("Шапки", 13)},
    )
    CategoryModelMPTT.objects.get_or_create(
        category_name="Ремені",
        parent=accessories,
        defaults={"display_order": 3, "slug": make_slug("Ремені", 14)},
    )
    CategoryModelMPTT.objects.get_or_create(
        category_name="Шкарпетки",
        parent=accessories,
        defaults={"display_order": 4, "slug": make_slug("Шкарпетки", 15)},
    )

    CategoryModelMPTT.objects.get_or_create(
        category_name="Куртки",
        parent=clothes,
        defaults={"display_order": 1, "slug": make_slug("Куртки", 16)},
    )
    CategoryModelMPTT.objects.get_or_create(
        category_name="Штани",
        parent=clothes,
        defaults={"display_order": 2, "slug": make_slug("Штани", 17)},
    )
    CategoryModelMPTT.objects.get_or_create(
        category_name="Футболки",
        parent=clothes,
        defaults={"display_order": 3, "slug": make_slug("Футболки", 18)},
    )
    CategoryModelMPTT.objects.get_or_create(
        category_name="Светри",
        parent=clothes,
        defaults={"display_order": 4, "slug": make_slug("Светри", 19)},
    )
    CategoryModelMPTT.objects.get_or_create(
        category_name="Термобілизна",
        parent=clothes,
        defaults={"display_order": 5, "slug": make_slug("Термобілизна", 20)},
    )


@shared_task
def create_products():
    sleep(5)
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


@shared_task
def delete_inactive_users():
    from django.contrib.auth.models import User

    deleted, _ = User.objects.filter(is_active=False).delete()
    print(f"Deleted {deleted} inactive users.")
