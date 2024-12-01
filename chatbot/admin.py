from django.contrib import admin
from .models import Bot, BotTemplate

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(BotTemplate)
class BotTemplateAdmin(admin.ModelAdmin):
    list_display = ("bot", "created_at", "updated_at")
    search_fields = ("bot",)
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")