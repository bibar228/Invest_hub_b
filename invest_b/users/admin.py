
from django.contrib import admin

# Register your models here.
from users.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', "login", "is_superuser", "is_staff", "is_active", "id"]

admin.site.register(User, UserAdmin)
