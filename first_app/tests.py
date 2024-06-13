from django.test import TestCase
from your_app.views import my_view  # Assuming my_view is in your_app.views

class ClientRegistrationTest(TestCase):

    def test_successful_registration(self):
        # Simulate form data for a new client
        client_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            # Add other required form fields
        }

        # Simulate a POST request with the form data
        request = self.client.post('/clients/register/', client_data)

        # Assert successful response (200 OK)
        self.assertEqual(request.status_code, 200)

        # You can add additional assertions here to verify specific behavior
        # For example, if the view redirects to a confirmation page:
        # self.assertRedirects(request, '/success/')

"""
bash:

pytest tests.py
"""
