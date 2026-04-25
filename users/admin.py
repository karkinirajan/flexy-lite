from django.contrib import admin

from .models import profile


@admin.register(profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__email")
