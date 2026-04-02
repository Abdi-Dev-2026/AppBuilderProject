from django.contrib import admin
from .models import App, UserActivity

# 1. Maamulka Apps-ka (Halkan waxaad ku arkeysaa Apps-ka la dhisay)
@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'slug', 'created_at') # Tiirarka kuu muuqanaya
    search_fields = ('name', 'owner__username') # Inaad magaca ama qofka ku raadin karto
    list_filter = ('created_at',) # Inaad waqtiga ku dhex sifeyn karto
    prepopulated_fields = {'slug': ('name',)} # Si iskeed ah u qoraysa slug-ga

# 2. Maamulka Dhaqdhaqaaqa (Halkan waxaad ku kormeereysaa isticmaalayaasha)
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    # Tiirarka ku tusaya qofka, waxa uu qabtay, app-ka uu taabtay, waqtiga iyo IP-ga
    list_display = ('user', 'action', 'app_name', 'timestamp', 'ip_address')
    
    # Inaad ku sifeyn karto waqtiga iyo nooca ficilka (Action)
    list_filter = ('timestamp', 'action')
    
    # Inaad ku raadin karto username-ka ama magaca app-ka
    search_fields = ('user__username', 'app_name')
    
    # Xogtan waa 'Read Only' si aan looga beddelin taariikhda dhabta ah ee dhacday
    readonly_fields = ('user', 'action', 'app_name', 'timestamp', 'ip_address')

    # In loo nidaamiyo xogta tii ugu dambeysay (Live Feed)
    ordering = ('-timestamp',)