from django import models  # Waa la hagaajiyay 'import超models'
from django import forms
from .models import SchoolProfile

class SchoolRegistrationForm(forms.ModelForm):
    # Fure sireedka maamulaha uu hadhow ku soo laaban doono
    secret_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Geli fure sireed kaaga gaarka ah'}),
        label="Fure Sireedka Iskuulka"
    )
    
    # Doorashada sanadaha rukunka (1 ilaa 10 Sano)
    YEAR_CHOICES = [(i, f"{i} Sano - ${i * 25}") for i in range(1, 11)]
    subscription_years = forms.ChoiceField(
        choices=YEAR_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'subscription_years_select'}),
        label="Muddada Rukunka"
    )

    class Meta:
        model = SchoolProfile
        # Haddii fields-kan (secret_password, subscription_years) aysan ku jirin Model-kaaga (SchoolProfile),
        # Waxay u baahan yihiin in halkan lagu daro si ay foomka ugu muuqdaan saxsan:
        fields = ['school_name', 'school_logo', 'secret_password', 'subscription_years', 'payment_method']
        widgets = {
            'school_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g. Al-Imra International'}),
            'school_logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }