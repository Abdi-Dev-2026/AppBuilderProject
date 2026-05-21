from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    App, UserActivity, SiteSetting, HomepageContent, TTSSetting,
    Quiz, Poll, Content, Like, Comment, ContactMessage, UserProfile,
    Subject, ExamYear, ReadingMaterial, QuizQuestion, GlobalNotice,
    ChatSetting, ChatMessage, FriendRequest  # Moodallada halkan ayaa lagu soo daray
)
# Soo dhoofinta resources-ka loogu talagalay Excel Import
from .resources import QuizQuestionResource, ReadingMaterialResource

# ---------------------------------------------------
# 0. BANAADIR EXAMS (INLINES & IMPORT/EXPORT)
# ---------------------------------------------------

# 1. Reading Material - Waxaa loogu daray Import/Export
@admin.register(ReadingMaterial)
class ReadingMaterialAdmin(ImportExportModelAdmin):
    resource_class = ReadingMaterialResource
    list_display = ('title', 'exam_year')
    search_fields = ('title', 'content')

# 2. Quiz Questions - Waxaa loogu daray Import/Export
@admin.register(QuizQuestion)
class QuizQuestionAdmin(ImportExportModelAdmin):
    resource_class = QuizQuestionResource
    list_display = ('question_text', 'exam_year', 'correct_option_index')
    search_fields = ('question_text',)

# Inlines loogu talagalay in lagu dhex arko gudaha ExamYear
class ReadingMaterialInline(admin.TabularInline):
    model = ReadingMaterial
    extra = 1

class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 5  

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_emoji')
    search_fields = ('name',)

    # Fieldsets loo sameeyay qaybaha cusub ee Emojis, Sawirada iyo Muuqaalada
    fieldsets = (
        ('Warbixinta Guud', {
            'fields': ('name', 'icon_emoji')
        }),
        ('Icon Sawir Ah (Image)', {
            'description': 'Haddii aad rabto sawir, dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('icon_image_file', 'icon_image_url')
        }),
        ('Icon Muuqaal Ah (Video)', {
            'description': 'Haddii aad rabto muuqaal, dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('icon_video_file', 'icon_video_url')
        }),
    )

@admin.register(ExamYear)
class ExamYearAdmin(admin.ModelAdmin):
    list_display = ('subject', 'year')
    list_filter = ('subject', 'year')
    inlines = [ReadingMaterialInline, QuizQuestionInline]

# ---------------------------------------------------
# 0.5. TTS SETTING ADMIN (CUSBOONAYSIINTA DHALADA & AVATARS)
# ---------------------------------------------------
@admin.register(TTSSetting)
class TTSSettingAdmin(admin.ModelAdmin):
    list_display = ('title', 'max_characters')
    
    fieldsets = (
        ('Xaddidaadda Qoraalka', {
            'fields': ('title', 'max_characters')
        }),
        ('Muuqaalka Gadaal (Background Media)', {
            'description': 'Muuqaalka ama sawirka dhalada ka dambeeya ee Interface-ka TTS',
            'fields': ('bg_image_file', 'bg_image_url', 'bg_video_file', 'bg_video_url')
        }),
        ('Avatar-ka Faiza (Codka Dumarka)', {
            'description': 'Sawirka ama Muuqaalka yar ee goobada ugu muuqanaya Faiza',
            'fields': ('faiza_avatar_image', 'faiza_avatar_video')
        }),
        ('Avatar-ka Maxamed (Codka Ragga)', {
            'description': 'Sawirka ama Muuqaalka yar ee goobada ugu muuqanaya Maxamed',
            'fields': ('maxamed_avatar_image', 'maxamed_avatar_video')
        }),
    )

# ---------------------------------------------------
# 1. USER PROFILE & FRIEND REQUESTS
# ---------------------------------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_id_code', 'first_name', 'father_name')
    search_fields = ('user__username', 'user_id_code', 'first_name')
    readonly_fields = ('user_id_code',)

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('sender__username', 'receiver__username')

# ---------------------------------------------------
# 2. APP ADMIN
# ---------------------------------------------------
@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'owner__username')
    list_filter = ('created_at',)

# ---------------------------------------------------
# 3. USER ACTIVITY ADMIN
# ---------------------------------------------------
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'app_name', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'action', 'app_name')
    readonly_fields = ('timestamp',)

# ---------------------------------------------------
# 4. SITE SETTINGS ADMIN
# ---------------------------------------------------
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('maintenance_mode', 'message')
    
    fieldsets = (
        ('Warbixinta Guud', {
            'fields': ('maintenance_mode', 'message')
        }),
        ('Sawirka (Image)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('image_file', 'image_url')
        }),
        ('Muuqaalka (Video)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('video_file', 'video_url')
        }),
    )

# ---------------------------------------------------
# 5. HOMEPAGE CONTENT ADMIN
# ---------------------------------------------------
@admin.register(HomepageContent)
class HomepageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
   
    fieldsets = (
        ('Warbixinta Guud', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Sawirka (Image)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('image_file', 'image_url')
        }),
        ('Muuqaalka (Video)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('video_file', 'video_url')
        }),
    )

# ---------------------------------------------------
# 6. CONTENT ADMIN
# ---------------------------------------------------
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'get_total_likes')
    search_fields = ('title', 'body_text')
    list_filter = ('created_at',)

    def get_total_likes(self, obj):
        return obj.total_likes
    get_total_likes.short_description = 'Total Likes'

    fieldsets = (
        ('Xogta Maqaalka', {
            'fields': ('title', 'body_text'),
        }),
        ('Sawirka (Image)', {
            'fields': ('image_file', 'image_url')
        }),
        ('Muuqaalka (Video)', {
            'fields': ('video_file', 'video_url')
        }),
        ('Xogta Kale', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at',)

# ---------------------------------------------------
# 7. LIKE & COMMENT ADMIN
# ---------------------------------------------------
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'text', 'created_at')
    search_fields = ('text', 'user__username')
    list_filter = ('created_at',)

# ---------------------------------------------------
# 8. QUIZ & POLL ADMIN
# ---------------------------------------------------
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('question', 'correct_answer', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('question',)

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'votes1', 'votes2')
    list_filter = ('is_active',)
    search_fields = ('question',)

# ---------------------------------------------------
# 9. CONTACT MESSAGE ADMIN
# ---------------------------------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at', 'is_read')
    readonly_fields = ('created_at',)
   
    fieldsets = (
        ('Xogta Farriinta', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at')
        }),
        ('Jawaab-celinta', {
            'fields': ('reply', 'is_read'),
        }),
    )

# ---------------------------------------------------
# 10. GLOBAL NOTICE ADMIN
# ---------------------------------------------------
@admin.register(GlobalNotice)
class GlobalNoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
   
    fieldsets = (
        ('Xogta Farriinta', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Sawirka (Image)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('image_file', 'image_url')
        }),
        ('Muuqaalka (Video)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('video_file', 'video_url', 'is_portrait')
        }),
    )

# ---------------------------------------------------
# 11. CHAT SETTING ADMIN (MAAMULISTA BACKGROUND-KA IYO CODKA)
# ---------------------------------------------------
@admin.register(ChatSetting)
class ChatSettingAdmin(admin.ModelAdmin):
    list_display = ('title', 'bg_type', 'is_video_muted') # Halkan waxaa lagu daray bg_type
    
    fieldsets = (
        ('Warbixinta Guud', {
            'fields': ('title', 'bg_type', 'is_video_muted') # Halkan waxaa lagu daray bg_type
        }),
        ('Muuqaalka Gadaal (Background Image)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link/URL',
            'fields': ('bg_image_file', 'bg_image_url')
        }),
        ('Muuqaalka Gadaal (Background Video)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link/URL',
            'fields': ('bg_video_file', 'bg_video_url')
        }),
    )

# ---------------------------------------------------
# 12. CHAT MESSAGE ADMIN (LA SOCASHADA FARIIMAHA DADKA)
# ---------------------------------------------------
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'short_message', 'has_media', 'timestamp')
    list_filter = ('timestamp', 'sender', 'receiver')
    search_fields = ('message', 'sender__username', 'receiver__username')
    readonly_fields = ('timestamp',)

    # Function si kooban u tusaya fariinta haddii ay dheer tahay
    def short_message(self, obj):
        if obj.message:
            return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
        return "[Media Only / Fayl oo kaliya]"
    short_message.short_description = 'Fariinta'

    # Hubinta nooca faylasha la soo raaciyay maadaama koodhka la isku daray
    def has_media(self, obj):
        status = []
        if obj.image: status.append("📷 Sawir")
        if obj.voice: status.append("🎤 Cod")
        if obj.attachment: 
            status.append("📁 Folder" if obj.is_folder else "📄 Fayl")
        
        return ", ".join(status) if status else "❌ Maya"
    has_media.short_description = 'Fayl / Media'