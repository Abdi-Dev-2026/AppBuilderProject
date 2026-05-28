from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import App

# 1. Form-ka lagu diiwaangeliyo User-ka (Nambar & Email)
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Telefoonka (Nambarkaaga)", 
        help_text="Fadlan geli nambarkaaga aqoonsiga (Tusaale: 061XXXXXXX)."
    )
    email = forms.EmailField(label="Email-ka", required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

# 2. Form-ka uu User-ku ku dhisayo App-kiisa
class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name', 'icon', 'image_url', 'download_link']
        labels = {
            'name': 'Magaca App-ka',
            'icon': 'Soo geli Icon (Sawir)',
            'image_url': 'Ama soo geli Link-ga sawirka (URL)',
            'download_link': 'Link-ga laga soo dejisto (Download Link)',
        }