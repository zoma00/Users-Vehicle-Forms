from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from phonenumbers import parse, region_code_for_number, is_valid_number
from phonenumbers import PhoneNumber


class CustomUser(AbstractUser):
    phone_number = PhoneNumber()
    email = models.CharField(max_length=255, unique=True, validators=[EmailValidator()])
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

    def validate_phone_number(phone_number):
        """
        Validates the phone number format (international).
        Raises a ValueError if the phone number is invalid.
        Returns the cleaned phone number (optional) upon success.
        """

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        try:
            phone_number_obj = parse(phone_number)
        except phonenumbers.NumberParseException:
            raise forms.ValidationError("Invalid phone number format")
        if not is_valid_number(phone_number_obj):
            raise forms.ValidationError("Invalid phone number format")
        country_code = region_code_for_number(phone_number_obj)
        return phone_number

        # No need to return here as validation is the focus

    def __str__(self):
        """
        Improved string representation of the user object.
        Includes username, name, phone number, address, and postal code.
        """

        # Approach 1: Using += for conditional concatenation
        address = f"{self.address_line1}"
        if self.address_line2:
            address += f", {self.address_line2}"
        if self.city:
            address += f", {self.city}"
        if self.state:
            address += f", {self.state}"
        if self.postal_code:
            address += f" {self.postal_code}"

        # Approach 2: Using conditional expression within f-string (alternative)
        # address = f"{self.address_line1}{', ' + self.address_line2 if self.address_line2 else ''}"

        return f"{self.username} ({self.first_name} {self.last_name}) - {self.phone_number} - {address}"


class Meta:
    verbose_name = "Custom User"  # Label for a single user
    verbose_name_plural = "Custom Users"  # Label for multiple users
