from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,TaxApplication
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']  

class TaxApplicationForm(forms.ModelForm):
    class Meta:
        model = TaxApplication
        fields =['application_type','id_card']