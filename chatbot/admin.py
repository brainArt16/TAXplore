from django.contrib import admin
from .models import *


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    
@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")

@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = [
        "collection_name",
        "description",
        "knowledge_base_type",
        "created_at",
        "is_active",
    ]
    list_filter = ["knowledge_base_type", "is_active"]
    search_fields = ["collection_name", "description"]
    ordering = ["collection_name"]


@admin.register(KnowledgeBaseDocument)
class KnowledgeBaseDocumentAdmin(admin.ModelAdmin):
    list_display = ["document", "knowledge_base", "created_at"]
    list_filter = ["knowledge_base"]
    search_fields = ["document"]

@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = ["bot", "created_at"]
    search_fields = ["bot"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at"]
    
@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name"]
    list_filter = ["created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    
@admin.register(BotSetting)
class BotSettingAdmin(admin.ModelAdmin):
    list_display = ["bot", "ai_model", "created_at", "updated_at"]
    search_fields = ["bot", "ai_model"]
    list_filter = ["created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]