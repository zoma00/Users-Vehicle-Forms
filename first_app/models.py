
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
import uuid

from loguru import logger
from structlog import getLogger
from phonenumbers import parse


class VehicleType(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField for auto-incrementing ID
    type_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type_name



    def save(self, *args, **kwargs):
        self.vin = self.generate_vin()  # Generate VIN before saving
        super().save(*args, **kwargs)


class Client(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField for auto-incrementing ID
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        max_length=128, unique=True, blank=True
    )  # Allow clients without email

    # Add address and phone number fields
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(
        max_length=100, blank=True
    )  # Allow for optional address line 2
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)  # Assuming US state format
    postal_code = models.CharField(max_length=10)
    phone_number = PhoneNumberField(blank=True,null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def save(self, *args, **kwargs):
        client_data = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "phone_number": self.phone_number,
        }
        # Filter out optional fields with a None value (if needed)
        # client_data = {k: v for k, v in client_data.items() if v is not None}

        super().save(*args, **kwargs)
        logger.info(f"Client data saved: {client_data}")

class Service(models.Model):
  """Model representing a service for a vehicle."""

  name = models.CharField(max_length=255)
  description = models.TextField(blank=True)
 
     
   # Adjust fields as needed

  # Add other relevant fields as needed, e.g., service_date, cost, etc.

  def __str__(self):
    return self.name 

class ServiceVIN(models.Model):
    vin = models.CharField(max_length=17, unique=True)


class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField for auto-incrementing ID

    type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)

    model_name = models.CharField(
        max_length=50, blank=True
    )  # Allow models without names

    year = models.IntegerField()

    client = models.ForeignKey(
        "Client", on_delete=models.CASCADE, blank=True, null=True
    )

    purchase_date = models.DateField(null=True, blank=True)

    color = models.CharField(max_length=50)

    engine_capacity = models.IntegerField()

    service_vin = models.ForeignKey(
        ServiceVIN, on_delete=models.CASCADE,blank=True,null=True
    )  # New foreign key
    services = models.ManyToManyField(Service, blank=True)

   
    def __str__(self):
        if self.model_name:
            return f"{self.type} {self.model_name} ({self.year})"
        else:
            return f"{self.type} ({self.year})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        logger.info(
            "vehicle_saved",  # Use "vehicle_saved" instead of "client_saved"
            vehicle_id=self.id,
            type=self.type.id,  # Access type through foreign key relationship
            model_name=self.model_name,
            year=self.year,
            client_id=self.client,  # Assuming a client_id field exists
            purchase_date=self.purchase_date,
            color=self.color,
            engine_capacity=self.engine_capacity,
            service_vin=self.service_vin,  # Access VIN from ServiceVIN
            )
       


        print(f"Vehicle saved: id={self.id}, type={self.type.id}, model_name={self.model_name},year={self.year},client={self.client},purchase_date={self.purchase_date}")



"""
 for services in self.services.all():
            logger.info(
            "associated_service",
            service_id=Service.id,
            service_name=Service.name,
            service_description=Service.description,
        )
    """
