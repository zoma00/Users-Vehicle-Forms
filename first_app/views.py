from logging import getLogger
from loguru import logger

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError  # Assuming you're using Django
from django.db import transaction
from django.forms import formset_factory


from first_app.models import VehicleType, Client, Vehicle, ServiceVIN,Service
from first_app.NewClientForm import NewClientForm  # Import the NewClientForm

from first_app.forms import VehicleForm, ServiceFormSet

from . import user_register  # Import login_view from the same module

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Hidden


# Create your views here.Test version
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('clients')
        else:
            # Handle failed login attempt
            error_message = "Invalid username or password. Please try again."
            login_dict = {'error_message': error_message}  # Create context with error message
            return render(request, 'first_app/login.html', context=login_dict)  # Render login.html with context
    else:
        # Render the login template
        return render(request,'first_app/login.html')

def purchased_clients(request):
    purchased_clients = Client.objects.order_by("first_name")
    vehicles = Vehicle.objects.all()
    success_message = messages.get_messages(request)

    client_dict = {"clients": purchased_clients, "vehicles": vehicles}
    return render(request, "first_app/clients.html", context=client_dict)
    """Handles client registration form and vehicle creation."""
    #logger = getLogger(__name__)  # Create a logger for this view


def register(request):
  if request.method == "POST":
    client_form = NewClientForm(request.POST)
    vehicle_form = VehicleForm(request.POST)
    service_formset = ServiceFormSet(request.POST)
    service_formset = ServiceFormSet(request.POST or None)


    helper = FormHelper()
    helper.layout = Layout(
      [Hidden('form-TOTAL_FORMS', '{{ service_formset.total_form_count }}'),
       Hidden('form-INITIAL_FORMS', '{{ service_formset.initial_form_count }}')],
      service_formset.forms,  # Include all service forms in the layout
    )
       

    if client_form.is_valid() and vehicle_form.is_valid() and service_formset.is_valid():
      with transaction.atomic():
        client = client_form.save()  # Save client first
        vehicle = vehicle_form.save()  # Don't save vehicle yet
        vehicle.client = client
        vehicle.save()  # Save vehicle first


        # Handle service VIN selection (similar to before)
        new_service_vin = vehicle_form.cleaned_data.get('new_service_vin')
        selected_service = vehicle_form.cleaned_data.get('service')

        # Save service VIN (if new)
        if new_service_vin:
          try:
            service_vin_obj = Service.objects.create(vin=new_service_vin)
            vehicle.service_vin = service_vin_obj
          except IntegrityError:
            messages.error(request, "This service VIN is already in use.")
            return render(request, "first_app/register.html", context={
              'client_form': client_form,
              'vehicle_form': vehicle_form,
              'service_formset': service_formset,
              'helper': helper
            })

        # Save selected service (if any)
        elif selected_service:
          vehicle.service_vin = selected_service

          vehicle.save()  # Now save the vehicle###

        # Save services from the formset
        for service_form in service_formset:
          service = service_form.save(commit=False)
          service.vehicle = vehicle  # Assign vehicle to each service
          service.save()

        messages.success(request, "Client and vehicle registered successfully!")
        logger.info(f"Client '{client_form.cleaned_data['first_name']}' registered successfully!")
        return redirect("clients")  # Redirect to the client list
    else:
      messages.error(request, f"Client form errors: {client_form.errors}")
      messages.error(request, f"Vehicle form errors: {vehicle_form.errors}")
      messages.error(request, f"Services form errors: {service_formset.errors}")
      print(f"services errors:{service_formset}")
  else:
    client_form = NewClientForm()
    vehicle_form = VehicleForm()
    service_formset = ServiceFormSet()

  context = {
    'client_form': client_form,
    'vehicle_form': vehicle_form,
    'service_formset': service_formset  ,  # Create an empty formset
 # Create an empty formset with prefix
    'helper': helper if request.method == 'POST' else None,  # Conditionally include helper
}

  return render(request, "first_app/register.html", context)


def my_view(request):
    # ... view logic    ...
    logger.info("User accessed view: %s", request.path)

    if request.method == 'POST':
        # Get client data from the form
        client_data = request.POST.dict()

        # Log client data in a structured format
        logger.debug(f"Client data submitted: {client_data}")

        # Validate client data (optional)
        # ... your data validation logic here ...

        try:
            # Create or update client based on form action (e.g., hidden field)
            if 'client_id' in client_data:  # Update existing client
                client = Client.objects.get(pk=client_data['client_id'])
                client.name = client_data['name']
                # ... update other fields based on form data ...
                client.save()
                message = 'Client updated successfully!'
            else:  # Create a new client
                client = Client.objects.create(**client_data)
                message = 'Client created successfully!'

            # Success response with a message
            context = {'message': message}
            return render(request, 'first_app/clients.html', context=context)

        except Exception as e:
            # Handle errors gracefully (e.g., database errors, validation errors)
            logger.error(f"Error processing client data: {e}")
            messages.error(request, f"An error occurred: {e}")  # Display error message to user
            return redirect('clients:list')  # Redirect to a list view for error handling

    else:  # Handle GET requests
        # ... your GET request logic here ...
        # You might want to retrieve existing client data for editing or display a list
        clients = Client.objects.all()
        vehicles = Vehicle.objects.all()
        context =  {'clients':clients, 'vehicles': vehicles}   # Empty context for GET requests (or customize as needed)
        return render(request, 'first_app/clients.html', context=context)



def logout_view(request):
    # Optionally redirect to a logout page or your app's homepage
    return redirect('login')

