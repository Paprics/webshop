import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from faker import Faker

CustomerUser = get_user_model()


class TestCustomerUser:

    # valid data
    PHONE = "+380991234567"
    EMAIL = "test@example.com"
    PASSWORD = "qwezxc123"

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "password_generator",
        [
            lambda: Faker().pystr(min_chars=0, max_chars=0),
            lambda: Faker().pystr(min_chars=129, max_chars=135),
        ],
    )
    def test_invalid_len_pass(self, password_generator):
        password = password_generator()
        customer = CustomerUser(
            phone_number=self.PHONE, email=self.EMAIL, password=password
        )
        with pytest.raises(ValidationError):
            customer.full_clean()

    @pytest.mark.django_db
    def test_max_length_name(self):
        fake = Faker()
        wrong_value = fake.pystr(min_chars=151, max_chars=160)
        customer = CustomerUser(
            phone_number=self.PHONE,
            email=self.EMAIL,
            password=self.PASSWORD,
            first_name=wrong_value,
            last_name=wrong_value,
        )

        with pytest.raises(ValidationError) as error_info:
            customer.full_clean()

        error_dict = error_info.value.message_dict
        assert "first_name" in error_dict
        assert "last_name" in error_dict

    @pytest.mark.django_db
    def test_createsuperuser(self):
        customer = CustomerUser.objects.create_superuser(
            self.PHONE, self.EMAIL, self.PASSWORD
        )
        db_customer = CustomerUser.objects.get(phone_number=self.PHONE)
        assert db_customer == customer
        assert db_customer.is_superuser is True
        assert db_customer.is_staff is True

    @pytest.mark.django_db
    def test_create_user(self):
        customer = CustomerUser.objects.create_user(
            self.PHONE, self.EMAIL, self.PASSWORD
        )
        db_customer = CustomerUser.objects.get(phone_number=self.PHONE)
        assert db_customer == customer
        assert db_customer.is_superuser is False
        assert db_customer.is_staff is False

    @pytest.mark.django_db
    def test_unique_phone(self):
        customer_1 = CustomerUser(
            phone_number=self.PHONE, email="ololo@gmail.com", password=self.PASSWORD
        )
        customer_1.full_clean()
        customer_1.save()

        customer_2 = CustomerUser(
            phone_number=self.PHONE,
            email="ololo-2025@gmail.com",
            password=self.PASSWORD,
        )
        with pytest.raises(ValidationError):
            customer_2.full_clean()

    @pytest.mark.xfail(reason="Уникальность email ????")
    @pytest.mark.django_db
    def test_unique_email(self):
        # TODO: fix uniqua emeil ????
        customer_1 = CustomerUser(
            phone_number="+380981234567", email=self.EMAIL, password=self.PASSWORD
        )
        customer_1.full_clean()
        customer_1.save()

        customer_2 = CustomerUser(
            phone_number="+380991234567", email=self.EMAIL, password=self.PASSWORD
        )
        with pytest.raises(ValidationError):
            customer_2.full_clean()

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "phone_number, email, password",
        [
            (None, EMAIL, PASSWORD),
            ("", EMAIL, PASSWORD),
            (PHONE, None, PASSWORD),
            (PHONE, "", PASSWORD),
            (PHONE, EMAIL, None),
            (PHONE, EMAIL, ""),
        ],
    )
    def test_missing_required_fields(self, phone_number, email, password):
        customer = CustomerUser(
            phone_number=phone_number, email=email, password=password
        )
        with pytest.raises(ValidationError):
            customer.full_clean()

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "phone_number",
        [
            "+38099123456",
            "+3809912345678",
            "12345",
            "hello",
            "+99999999999999999999",
        ],
    )
    def test_invalid_phone(self, phone_number):
        customer = CustomerUser(
            phone_number=phone_number, email=self.EMAIL, password=self.PASSWORD
        )
        with pytest.raises(ValidationError):
            customer.full_clean()

    @pytest.mark.django_db
    @pytest.mark.parametrize("email", ["", None, "exzamplgmail.com"])
    def test_invalid_email(self, email):
        customer = CustomerUser(
            phone_number=self.PHONE, email=email, password=self.PASSWORD
        )
        with pytest.raises(ValidationError):
            customer.full_clean()

    @pytest.mark.django_db
    def test_valid_data(self):
        customer = CustomerUser(
            phone_number=self.PHONE, email=self.EMAIL, password=self.PASSWORD
        )
        customer.full_clean()
        customer.save()
        assert CustomerUser.objects.filter(phone_number=self.PHONE).exists()
