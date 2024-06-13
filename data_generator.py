import os
import random
import uuid

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "first_pro.settings")
import django
django.setup()
from faker import Faker

from phonenumbers import parse, PhoneNumberFormat, geocoder

from datetime import datetime, timedelta
from first_app.models import Vehicle, Client, VehicleType, ServiceVIN
import time
import phonenumbers




# Initialize data generation tools
fake = Faker()

color_options = [
    "Red",
    "Blue",
    "Black",
    "Silver",
    "Gray",
    "White",
]  # Example color list

# Vehicle type list
vehicle_type_choices = ["Car", "Truck", "Motorcycle", "SUV"]
# Create vehicle types if none exist (optional)
if not VehicleType.objects.exists():
    for type_name in vehicle_type_choices:
        VehicleType.objects.create(type_name=type_name)
# Car manufacturer list (modify and expand as needed)
manufacturer_list = ["Toyota", "Honda", "BMW", "Fiat"]

# Gen Random vins uuid
def generate_random_vin():
    return str(uuid.uuid4())[:17]  # Generate 17-character VIN

def populate(
    num_vehicles=None,
    min_purchase_date=None,
    max_purchase_date=None,
    model_name_distribution=None,
    color_list=None,
):
    """
    Generates random vehicle and client data, creating objects in the database.

    Args:
        num_vehicles (int, optional): The number of vehicles to generate. Defaults to defined value.
        min_purchase_date (datetime.datetime, optional): The minimum date for the purchase range.
            Defaults to defined value.
        max_purchase_date (datetime.datetime, optional): The maximum date for the purchase range.
            Defaults to defined value.
        model_name_distribution (dict, optional): A dictionary specifying the probability
            of generating a specific car manufacturer's model. Defaults to None (uniform distribution).
        color_list (list, optional): A list of color options for vehicles. Defaults to defined value.
    """
    
    if not num_vehicles:
        num_vehicles = num_vehicles  # Use defined default value
    if not min_purchase_date:
        min_purchase_date = min_purchase_date  # Use defined default value
    if not max_purchase_date:
        max_purchase_date = max_purchase_date  # Use defined default value

    if min_purchase_date is not None and max_purchase_date is not None:
        if min_purchase_date > max_purchase_date:
            raise ValueError(
                "Minimum purchase date cannot be after maximum purchase date."
            )

    for _ in range(num_vehicles):
        # Generate random manufacturer based on distribution (if provided)
        if model_name_distribution:
            random_manufacturer = random.choices(
                population=manufacturer_list, weights=model_name_distribution.values()
            )[0]
        else:
            random_manufacturer = random.choice(manufacturer_list)

        # Generate random model name using faker (assuming model names exist for chosen manufacturer)
        # Modify this line if your model name generation logic differs
        random_model_name = f"{random_manufacturer} {fake.word()}"

        # Generate random client data
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()

        # Generate phone number with extension
        phone_number_with_extension = fake.phone_number()
        # Parse phone number and handle exceptions
        try:
            parsed_number = parse(phone_number_with_extension)
            core_phone_number = parsed_number.national_number
        except phonenumbers.phonenumberutil.NumberParseException as e:
            print(f"Error parsing phone number: {phone_number_with_extension}")
            core_phone_number = ""  # Assign empty string for parsing errors
        # Ensure core_phone_number is a string (if not None)
        if core_phone_number is not None:
            core_phone_number = str(core_phone_number)

         # Generate address
        address_line1 = fake.street_address()
        city = fake.city()
        state = fake.state()
        postal_code = fake.postalcode()

        # Create Client object with core phone number
        client = Client.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=core_phone_number,  # Assign extracted core phone number
            address_line1=address_line1,
            city=city,
            state=state,
            postal_code=postal_code,
        )

        # Generate random vehicle details
        # Use existing vehicle types
        vehicle_type = random.choice(VehicleType.objects.all())
        year = random.randint(2010, 2024)  # Random year (adjust range as needed)
        random_engine_capacity = random.randint(1000, 5000)  # Modify range as needed
        random_color = random.choice(color_options)

        # Generate a random purchase date within a specified range
        min_purchase_date = datetime(2010, 1, 1)  # Adjust as needed
        max_purchase_date = datetime.now()  # Set to today's date
        random_days = random.randint(0, (max_purchase_date - min_purchase_date).days)
        purchase_date = min_purchase_date + timedelta(days=random_days)

        # Generate a random VIN (consider production-grade alternatives)
        unique_vin = generate_random_vin()

        # Create a ServiceVIN instance with the generated VIN
        service_vin_obj = ServiceVIN.objects.create(vin=unique_vin)
        #  Create  VehicleType instance
        vehicle_type_instance, _ = VehicleType.objects.get_or_create(
            type_name=vehicle_type
        )

        # Create the Vehicle instance
        vehicle = Vehicle.objects.create(
            type=vehicle_type_instance,
            model_name=random_model_name,
            year=year,
            engine_capacity=random_engine_capacity,
            purchase_date=purchase_date,
            color=random_color,
            service_vin=service_vin_obj,  # Assign the created service_vin
        )

        # Optionally, assign the client to the vehicle (assuming a foreign key relationship)
        vehicle.client = client
        vehicle.save()

        start_time = time.time()  # Capture start time for progress calculation

    for i in range(num_vehicles):
        # Implement your logic to generate and save vehicle/client data here

        # Print progress update every 100 iterations or at the end (modify as needed)
        if (i % 25 == 0) or (i == num_vehicles - 1):
            progress = (i + 1) / num_vehicles * 100
            elapsed_time = time.time() - start_time
            print(
                f"Progress: {progress:.2f}%, Elapsed Time: {elapsed_time:.2f} seconds"
            )


if __name__ == "__main__":
    # Example usage with default parameters
    populate(num_vehicles= 5)

    # Example usage with custom parameters
    custom_params = {
        "num_vehicles": 5,
        "min_purchase_date": datetime(2015, 1, 1),
        "max_purchase_date": datetime(2020, 12, 31),
        "model_name_distribution": {
            "Toyota": 0.5,
            "Honda": 0.3,
            "BMW": 0.1,
            "Fiat": 0.1,
        },
    }

    populate(**custom_params)  # Pass arguments as keyword arguments
