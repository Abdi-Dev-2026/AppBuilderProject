from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Waxaan ka soo dhoofsanaynaa app-ka rasmiga ah ee profile_html
from profile_html.models import UserProfile

# ---------------------------------------------------
# USER REGISTER FORM (STABLE + NO INTEGRITY ERROR)
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

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'father_name',
            'grandfather_name',
            'password1',
            'password2'
        ]

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

            # ✅ XALKA CILADDA INTEGRITY ERROR: 
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            # Xogta ku dar profile-ka jira ama kan cuzub ee dhashay
            profile.first_name = self.cleaned_data['first_name']
            profile.father_name = self.cleaned_data['father_name']
            profile.grandfather_name = self.cleaned_data['grandfather_name']
            profile.save()

        return user