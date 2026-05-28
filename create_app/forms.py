from django import forms
# Waxaan ka soo dhoofsanaynaa model-ka App ee ku dhex jira isla app-kaan create_app
from .models import App

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

    # ---------------------------------------------------
    # 🔥 VALIDATION: ICON vs IMAGE_URL
    # ---------------------------------------------------
    def clean(self):
        cleaned_data = super().clean()
        icon = cleaned_data.get('icon')
        image_url = cleaned_data.get('image_url')

        if not icon and not image_url:
            raise forms.ValidationError("Fadlan geli sawir ama link sawir.")

        return cleaned_data