from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from phonenumbers import parse, region_code_for_number, is_valid_number

from .models import Client, Vehicle,ServiceVIN,VehicleType,Service 
from first_app.NewClientForm import NewClientForm  # Import the NewClientForm

from django.forms import formset_factory
from django.forms import ModelForm, modelformset_factory

from django.forms import BaseFormSet

from bootstrap_datepicker_plus.widgets import DatePickerInput



class ClientForm(forms.ModelForm):
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

    def clean_email(self):
        """
        Custom validation method to check for unique email addresses.
        Raises a ValidationError if the email already exists in the database.
        """
        email = self.cleaned_data[
            "email"
        ].lower()  # Convert email to lowercase for case-insensitive check
        if Client.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def clean(self):
        """
        Custom validation to check if both first name and last name are provided.
        Raises a ValidationError if either is missing.
        """
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if not first_name or not last_name:
            raise forms.ValidationError("Please provide both first and last name.")

        return cleaned_data


def clean_phone_number(self):
    """
    Custom validation method to check for valid phone number format.
    Raises a ValidationError if the phone number is invalid.
    """
    phone_number = self.cleaned_data["phone_number"]

    # Parse the phone number and automatically detect the country code
    try:
        phone_number_obj = parse(phone_number)
    except phonenumbers.NumberParseException:
        raise forms.ValidationError("Invalid phone number format")

    if not is_valid_number(phone_number_obj):
        raise forms.ValidationError("Invalid phone number format")

    # You can optionally access the country code here
    # country_code = region_code_for_number(phone_number_obj)

    # Return the cleaned phone number (optional)
    return phone_number




class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description']  # Replace "..." with your actual field names


ServiceFormSet = modelformset_factory(Service, fields=['name', 'description'], extra=2)



    

class VehicleForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False)
    new_service_vin = forms.CharField(required=False, label="New Service VIN")  # Allow entering a new VIN
    service = forms.ModelChoiceField(queryset=ServiceVIN.objects.all(), required=False, label="Existing Service VIN")

    class Meta:
        model = Vehicle
        fields = [
            "type",
            "model_name",
            "year",
            "engine_capacity",
            "color",
            "client",
            "purchase_date",
            "service_vin",
        ]

        labels = {
            "type" :"Type",
            "model_name":"Model Name",   
            "year" :"Year",
            "engine_capacity":"Engin Capacity",
            "color":'color',
            "client":'client',
            "purchase_date":'Purshased Date',
            "service_vin" :'ServiceVin',
            "service_formset": "Services"
        }

    def save(self, commit=True):
        purchase_date = self.cleaned_data["purchase_date"]

        vehicle = super().save(commit=commit)  # Save vehicle data first

        # Handle single service selection from service field
        selected_service = self.cleaned_data.get("service_formset")
        vehicle.services.add(selected_service) ##

        # Handle adding new services (if applicable)
        service_formset = self.cleaned_data.get("service_formset")
        if service_formset and service_formset.is_valid():
          for service_form in service_formset:
            services = service_form.save(commit=False)  # Save service instance without saving to DB yet
            services.vehicle = vehicle  # Link new service to the vehicle
            services.save()  # Now save the linked service

        return vehicle


def clean_service_vin(self):
    service_vin = self.cleaned_data.get('service_vin')

    # Handle None values gracefully
    if service_vin is None:
        return service_vin  # Allow empty service VIN

    is_faker_generated = getattr(service_vin, 'is_faker_generated', False)  # Access attribute if available

    if not is_faker_generated and ServiceVIN.objects.filter(pk=service_vin.pk).exists():
        raise forms.ValidationError("This service VIN is already in use. Please choose a unique one.")
    return service_vin
     

def clean_purchase_date(self):
    purchase_date = self.cleaned_data["purchase_date"]

    # Check for required field
    if purchase_date is None:
        raise forms.ValidationError("Purchase date is required.")

    try:
        # Assuming date input is a string, attempt conversion to datetime object
        parsed_date = datetime.datetime.strptime(purchase_date, "%Y-%m-%d").date()
        return parsed_date
    except ValueError:
        # Raise validation error if format is incorrect
        raise forms.ValidationError("Invalid date format. Please enter in YYYY-MM-DD format (e.g., 2024-05-13).")
    


"""

ServiceFormSet = modelformset_factory(
    Service,
    form=ServiceForm,
)
"""
   
