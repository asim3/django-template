from django.contrib.admin import register, ModelAdmin
from .models import Profile


@register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ("user", "phone", "is_email_verified",)
    list_filter = ("is_email_verified",)
    search_fields = ("phone",)
