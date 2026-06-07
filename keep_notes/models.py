from django.db import models
from django.contrib.auth.models import User
# Waxaan soo dhoofsanaynaa Profile-ka si aan u isticmaalno user_id_code
from profile_html.models import UserProfile

class Note(models.Model):
    # Ku xidh note kasta isticmaalaha rasmiga ah
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notes')
    
    # Qaybaha Note-ka (Cinwaan iyo Qoraalka weyn)
    title = models.CharField(max_length=255, blank=True, verbose_name="Cinwaanka")
    content = models.TextField(blank=True, verbose_name="Qoraalka Note-ka")
    
    # Faylasha la soo gelin karo (Sawirro, PDF, Muuqaalo)
    file_attachment = models.FileField(upload_to='keep_notes_files/', blank=True, null=True, verbose_name="Faylka Lifaaqa ah")
    
    # Wakhtiga la sameeyay iyo wakhtiga la wax ka beddelay (Muhiim u ah isku-sync-gelyada)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Wakhtiga la abuuray")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Wakhtiga la cusboonaysiiyay")
    
    # Aaladda uu qofku ka soo qoray xogta (Mobile mise Laptop) - Si Admin-ku ula socdo
    device_info = models.CharField(max_length=100, blank=True, null=True, verbose_name="Aaladda laga soo qoray")

    class Meta:
        ordering = ['-updated_at'] # Had iyo jeer kan ugu dambeeya ha soo hor baxo

    def __str__(self):
        return f"Note: {self.title or 'Bilaa Cinwaan'} - {self.user_profile.user_id_code}"