from django.contrib.admin import register, ModelAdmin
from .models import User

@register(User)
class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('is_superuser', 'is_active')
