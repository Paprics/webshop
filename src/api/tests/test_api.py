import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from api import views
from common.models import Content


@pytest.fixture
def create_content(db):
    content = Content.objects.create(
        title="Test title text",
        slug="test_slug",
        content="Test content text",
        is_published=True,
    )
    return content


@pytest.fixture
def admin_client(db):
    User = get_user_model()
    user = User.objects.create_user(
        password="adminpass",
        phone_number="+380991234567",
        email="user5@example.com",
    )
    user.is_staff = True
    user.save()

    admin = APIClient()
    admin.force_authenticate(user=user)
    return admin


@pytest.fixture
def customer_client(db):
    User = get_user_model()
    user = User.objects.create_user(
        password="adminpass",
        phone_number="+380991234568",
        email="user4@example.com",
    )
    user.is_staff = False
    user.save()

    customer = APIClient()
    customer.force_authenticate(user=user)
    return customer


@pytest.fixture
def set_customer(db):
    User = get_user_model()

    user_1 = User.objects.create_user(
        phone_number="+380991234561",
        email="user1@example.com",
        password="test_pass",
    )
    user_2 = User.objects.create_user(
        phone_number="+380991234562",
        email="user2@example.com",
        password="test_pass",
    )
    user_3 = User.objects.create_user(
        phone_number="+380991234563",
        email="user3@example.com",
        password="test_pass",
    )

    customer_1 = APIClient()
    customer_2 = APIClient()
    customer_3 = APIClient()

    customer_1.force_authenticate(user=user_1)
    customer_2.force_authenticate(user=user_2)
    customer_3.force_authenticate(user=user_3)

    return {
        "customer_1": customer_1,
        "customer_2": customer_2,
        "customer_3": customer_3,
    }


@pytest.mark.django_db
class TestContentAPI:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        get_user_model().objects.all().delete()

    def test_get_content(self, admin_client, customer_client, create_content):

        response = APIClient().get("/api/v1/content/", format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["title"] == create_content.title

        response = customer_client.get("/api/v1/content/", format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["title"] == create_content.title

    def test_get_detail_content(self, admin_client, customer_client, create_content):
        url_content = f"/api/v1/content/{create_content.slug}/"

        for client in (APIClient(), customer_client, admin_client):
            response = client.get(url_content, format="json")
            assert response.status_code == status.HTTP_200_OK
            assert response.data["title"] == create_content.title
            assert response.data["content"] == create_content.content

    def test_CRUD_content(self, admin_client, customer_client, create_content):

        for client in (APIClient(), customer_client):
            response = client.post("/api/v1/content/", data={}, format="json")
            assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

        data = {"title": "Test title_1", "slug": "test_slug_1", "content": "Test content text"}

        response = admin_client.post("/api/v1/content/", data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == data["title"]

        response = admin_client.get(f"/api/v1/content/{data['slug']}/", format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == data["title"]

        patch_data = {"title": "Test title_3"}
        response = admin_client.patch(f"/api/v1/content/{data['slug']}/", data=patch_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == patch_data["title"]

        response = admin_client.delete(f"/api/v1/content/{data['slug']}/", format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = admin_client.get(f"/api/v1/content/{data['slug']}/", format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCustomerAPI:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        get_user_model().objects.all().delete()

    @pytest.mark.django_db
    def test_customer_CRUD(self, admin_client, customer_client, set_customer):
        client = APIClient()
        response_user = client.post(
            "/api/v1/customer/",
            data={"phone_number": "+380997654321", "password": "test_pass", "email": "test@test.test"},
            format="json",
        )
        assert response_user.status_code == status.HTTP_201_CREATED

        user_id = response_user.data["id"]

        response = admin_client.get(f"/api/v1/customer/{user_id}/", format="json")
        assert response.status_code == status.HTTP_200_OK

        response = admin_client.patch(f"/api/v1/customer/{user_id}/", data={"email": "test@test.test"}, format="json")
        assert response.status_code in (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT)
        assert response.data["email"] == "test@test.test"

        response = admin_client.delete(f"/api/v1/customer/{user_id}/", format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = admin_client.get(f"/api/v1/customer/{user_id}/", format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.xfail(reason="fail on Postgres")
    @pytest.mark.django_db
    def test_customer_detail(self, admin_client, customer_client, set_customer):
        # Unauthenticated client (anonymous user)
        response = APIClient().get("/api/v1/customer/1/")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data

        # Authenticated client (regular user)
        response = customer_client.get("/api/v1/customer/1/")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data

    @pytest.mark.xfail(reason="fail on Postgres")
    @pytest.mark.django_db
    def test_get_list_customer_data(self, admin_client, customer_client, set_customer):
        response = admin_client.get("/api/v1/customer/")
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        expected_count = get_user_model().objects.count()
        assert len(data["results"]) == expected_count

        response = customer_client.get("/api/v1/customer/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = admin_client.get("/api/v1/customer/1/")
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data

        response = customer_client.get("/api/v1/customer/1/")
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data

    @pytest.mark.django_db
    def test_get_list_customer_status_code(self, admin_client, customer_client):
        factory = APIRequestFactory()
        request = factory.get("/api/v1/customer/")

        # Unauthenticated client (anonymous user)
        request.user = AnonymousUser()
        view = views.CustomerListCreateView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, "CustomerListCreateView: 401"

        # Authenticated client (regular user)
        response = customer_client.get("/api/v1/customer/")
        assert response.status_code == status.HTTP_403_FORBIDDEN, "CustomerListCreateView: 403"

        # Admin
        response = admin_client.get("/api/v1/customer/")
        assert response.status_code == status.HTTP_200_OK, "CustomerListCreateView: 200"

    @pytest.mark.xfail(reason="fail on Postgres")
    @pytest.mark.django_db
    def test_get_user(self):
        factory = APIRequestFactory()
        request = factory.post(
            "customer",
            data={"phone_number": "+380991234567", "password": "test_pass", "email": "testemail@test.com"},
            format="json",
        )
        view = views.CustomerListCreateView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED, "MemberListCreateView: 201 для создания кастомера"

        request = factory.get("/api/v1/customer/1")
        view = views.CustomerDetailView.as_view()
        response = view(request, pk=1)

        assert response.status_code == status.HTTP_200_OK, "MemberDetailView: 200 для запроса костомера"

    @pytest.mark.django_db
    def test_get_wrong_customer(self):
        factory = APIRequestFactory()
        request = factory.get("/api/v1/customer/1")

        view = views.CustomerDetailView.as_view()
        response = view(request, pk=1)

        assert (
            response.status_code == status.HTTP_404_NOT_FOUND
        ), "test_get_wrong_customer: 404 для несуществующего юзера"

    @pytest.mark.django_db
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(phone_number="+380997654321", password="pass123")
        assert user.phone_number == "+380997654321"
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.check_password("pass123") is True

    @pytest.mark.django_db
    def test_create_superuser(self):
        User = get_user_model()
        admin = User.objects.create_superuser(phone_number="+380987654321", password="adminpass")
        assert admin.phone_number == "+380987654321"
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.check_password("adminpass") is True
