from django.contrib import admin
from .models import  Category, AiTip, MerchantMapping, Notification




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "user", "created_at")
    search_fields = ("name", "user__username")
    list_filter = ("type", "created_at")
    ordering = ("-created_at",)


@admin.register(AiTip)
class AiTipAdmin(admin.ModelAdmin):
    list_display = ("text", "locale", "created_at")
    search_fields = ("text", "locale")
    list_filter = ("locale",)
    ordering = ("-created_at",)


@admin.register(MerchantMapping)
class MerchantMappingAdmin(admin.ModelAdmin):
    list_display = ("keyword", "category_name", "category_type", "priority")
    search_fields = ("keyword", "category_name")
    list_filter = ("category_type",)
    ordering = ("-priority", "keyword")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "read", "created_at")
    search_fields = ("title", "body", "user__username")
    list_filter = ("read", "created_at")
    ordering = ("-created_at",)
