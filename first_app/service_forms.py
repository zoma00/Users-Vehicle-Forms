from django import forms
from .models import Service  # Assuming your Service model is in the same app

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description']  # Adjust fields as needed

        # Make the 'name' field required
    #    widgets = {
     #       'name': forms.TextInput(attrs={'required': True}),
    #    }
