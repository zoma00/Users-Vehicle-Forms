from django import forms
from .models import Client  # Assuming your Client model is in models.py

class NewClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "first_name",
            "last_name",
            "email",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "postal_code",
            "phone_number",
        ]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Enter your email"}),
        }
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
            "address_line1": "Address Line 1",
            "address_line2": "Address Line 2",
            "city": "City",
            "state": "State",
            "postal_code": "Postal Code",
            "phone_number": "Phone Number",
        }
