from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class SchoolProfile(models.Model):
    # Wuxuu si toos ah ugu xirmayaa User-ka nidaamkaaga weyn ee wata ID Code-ka
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schools')
    school_name = models.CharField(max_length=255, unique=True)
    school_logo = models.ImageField(upload_to='school_logos/', null=True, blank=True)
    secret_password = models.CharField(max_length=100) # Fure sireedka maamulaha uu hadhow ku soo laaban doono
    
    # Qaybta rukunka (Subscription)
    subscription_years = models.IntegerField(default=1)
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2, default=25.00)
    payment_method = models.CharField(max_length=50, choices=[('evc_plus', 'EVC Plus'), ('edahab', 'eDahab')])
    
    # Khadkan cusub ee lambarka lacagta laga soo diray:
    sender_phone_number = models.CharField(max_length=20, null=True, blank=True) 
    
    is_active = models.BooleanField(default=False) # Admin-ka sare (adiga) ayaa ka dhigi kara True marka lacagtu soo dhacdo
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Marka ugu horreysa ee la kaydinayo, si toos ah u xisaabi taariikhda uu ka dhacayo rukunka
        if not self.id:
            self.expires_at = timezone.now() + datetime.timedelta(days=365 * self.subscription_years)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.school_name


class StudentResult(models.Model):
    LEVEL_CHOICES = [
        ('dhexe', 'Dugsi Dhexe (8 Maado)'),
        ('sare', 'Dugsi Sare (12 Maado)'),
    ]

    # Arday kasta wuxuu ku xiran yahay iskuulka soo geliyay xogtiisa
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE, related_name='students')
    full_name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=50, unique=True) # Roll Number-ka nidaamku u dhalinayo
    school_level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='dhexe')
    
    # 1. Maadooyinka Dugsiga Dhexe & Sare (Wadaagga ah)
    tarbiyo = models.CharField(max_length=5, default='D-')
    carabi = models.CharField(max_length=5, default='D-')
    af_soomaali = models.CharField(max_length=5, default='D-')
    xisaab = models.CharField(max_length=5, default='D-')
    ingiriisi = models.CharField(max_length=5, default='D-')
    teknooloji = models.CharField(max_length=5, default='D-')
    
    # 2. Maadooyinka gaarka u ah Dugsiga Dhexe oo kaliya
    cilmi_bulsho = models.CharField(max_length=5, default='D-', null=True, blank=True)
    saynis = models.CharField(max_length=5, default='D-', null=True, blank=True)
    
    # 3. Maadooyinka gaarka u ah Dugsiga Sare oo kaliya (Si ay 12 Maado u buuxsanto)
    biology = models.CharField(max_length=5, default='D-', null=True, blank=True)
    chemistry = models.CharField(max_length=5, default='D-', null=True, blank=True)
    physics = models.CharField(max_length=5, default='D-', null=True, blank=True)
    juqraafi = models.CharField(max_length=5, default='D-', null=True, blank=True)
    taariikh = models.CharField(max_length=5, default='D-', null=True, blank=True)
    business = models.CharField(max_length=5, default='D-', null=True, blank=True)
    
    # Xogta Natiijada kama dambaysta ah
    celceliska = models.CharField(max_length=5, default='D-') # Tusaale: B-, A, C+
    goaan = models.CharField(max_length=20, default='Gudbay') # Gudbay ama Haray
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.roll_number}) - {self.school.school_name}"