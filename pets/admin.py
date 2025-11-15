from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "available", "stock", "created_at")
    list_filter = ("available",)
    search_fields = ("name", "description")
    ordering = ("name",)