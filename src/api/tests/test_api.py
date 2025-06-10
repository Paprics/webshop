import pytest
from rest_framework.test import APIClient

from accounts.models import CustomerUser


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "phone_number": "+380991234567",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpassword123",
    }


@pytest.mark.django_db
def test_create_customer_user(api_client, user_data):
    response = api_client.post("/api/v1/member/", user_data)
    assert response.status_code == 201
    assert CustomerUser.objects.filter(phone_number=user_data["phone_number"]).exists()


@pytest.mark.django_db
def test_get_category_list(api_client):
    response = api_client.get("/api/v1/category/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_content_list(api_client):
    response = api_client.get("/api/v1/content/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_product_list(api_client):
    response = api_client.get("/api/v1/products/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_product_detail_404(api_client):
    response = api_client.get("/api/v1/products/non-existent-slug/")
    assert response.status_code == 404
