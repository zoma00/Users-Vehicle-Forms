from django.urls import path
from first_app import views

app_name = 'first_app'
urlpatterns = [
    path('login/', views.login_user, name='login'),  # Use login_view for root URL

]		  


