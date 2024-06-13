from django.urls import path
from django.shortcuts import render, redirect
from . import user_register  # Import user_register from the same module
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth import get_user_model, login




def user_register(request):
    User = get_user_model()  # Now use your custom model

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')  # Get phone number
        address_line1 = request.POST.get('address_line1')  # Get address fields
        address_line2 = request.POST.get('address_line2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')

        # Check for missing fields (optional)
        if not all([username, email, password, phone_number, address_line1, city, state, postal_code]):
            # Handle missing field error
            return render(request, 'first_app/user_register.html', {'error': 'Please fill out all required fields'})

        try:
            user = CustomUser.objects.create_user(
                username=username, email=email, password=password,
                phone_number=phone_number,  # Add custom fields
                address_line1=address_line1,
                address_line2=address_line2,
                city=city,
                state=state,
                postal_code=postal_code
            )
            login(request, user)
            return redirect('first_app:index')
        except IntegrityError:
            # Handle duplicate email error
            return render(request, 'first_app/user_register.html', {'error': 'Email address already exists'})
    else:
        return render(request, 'first_app/user_register.html')



