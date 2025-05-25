from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from accounts.utils.manegers import CustomerManager

# Create your models here.
from django.contrib.auth.models import User
class CustomerUser(AbstractBaseUser, PermissionsMixin):
    # from django.contrib.auth.models import User --> Base Model User
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    phone_number = PhoneNumberField(
        _("phone number"),
        unique=True,
        help_text=_(
            "Required. Enter phone number in international format starting with + and country code, e.g. +380..."
        ),
        error_messages={"unique": _("A user with that phone number already exists.")},
    )

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"))

    is_staff = models.BooleanField(
        _("staff status"), default=False, help_text=_("Designates whether the user can log into this admin site.")
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomerManager()

    # Field used for login (sign-in, authentication)
    USERNAME_FIELD = "phone_number"

    # Field representing the email address, so Django knows where to find it
    EMAIL_FIELD = "email"

    # Fields required only when creating a superuser via createsuperuser command
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("customer")
        verbose_name_plural = _("costomers")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class ProfileCustomer(models.Model):
    class Meta:
        db_table = 'profile_customer'
        verbose_name = _("profile customer")
        verbose_name_plural = _("profile customers")

    customer = models.OneToOneField('CustomerUser', on_delete=models.CASCADE, related_name='profile')
    delivery_address = models.TextField(max_length=500)
    additional_contacts = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.customer.phone_number}'