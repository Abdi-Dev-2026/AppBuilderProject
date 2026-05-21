from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import App, UserProfile

# ---------------------------------------------------
# USER REGISTER FORM (STABLE + NO VALIDATION ERROR)
# ---------------------------------------------------
class UserRegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Geli email-kaaga'})
    )

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Magacaaga'})
    )

    father_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Magaca Aabbaha'})
    )

    grandfather_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Magaca Awoowaha'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Halkan waxaan ku daraynaa field-yadaada gaarka ah annagoo ka fogaanayna password-ka gacanta laga qoro
        fields = UserCreationForm.Meta.fields + (
            'email',
            'first_name',
            'father_name',
            'grandfather_name',
        )

    # ---------------------------------------------------
    # 🔥 SAVE USER + PROFILE (FIXED INTEGRITY ERROR)
    # ---------------------------------------------------
    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email']

        # 🔄 USERNAME UNIQUE LOGIC
        username = email
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{email}_{counter}"
            counter += 1

        user.username = username
        user.email = email
        user.first_name = self.cleaned_data['first_name']

        if commit:
            user.save()

            # ✅ XALKA CILADDA: get_or_create
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            profile.first_name = self.cleaned_data['first_name']
            profile.father_name = self.cleaned_data['father_name']
            profile.grandfather_name = self.cleaned_data['grandfather_name']
            profile.save()

        return user


# ---------------------------------------------------
# APP FORM (VALIDATION IMPROVED)
# ---------------------------------------------------
class AppForm(forms.ModelForm):

    class Meta:
        model = App
        fields = ['name', 'icon', 'image_url', 'download_link']

        labels = {
            'name': 'Magaca App-ka',
            'icon': 'Soo geli Icon (Sawir)',
            'image_url': 'Ama geli Link-ga sawirka (URL)',
            'download_link': 'Link-ga Download-ka',
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Magaca App-ka'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
            'download_link': forms.URLInput(attrs={'placeholder': 'https://...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        icon = cleaned_data.get('icon')
        image_url = cleaned_data.get('image_url')

        if not icon and not image_url:
            raise forms.ValidationError("Fadlan geli sawir ama link sawir.")

        return cleaned_data