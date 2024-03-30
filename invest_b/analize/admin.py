from django.contrib import admin

# Register your models here.
from analize.models import Siggs


class UserAdmin(admin.ModelAdmin):
    list_display = ['cryptocode', "trade_position", "signal_owner"]

admin.site.register(Siggs, UserAdmin)
