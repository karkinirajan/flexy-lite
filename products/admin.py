from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("p_sku", "quantity", "location", "action", "date_created")
    search_fields = ("p_sku", "description", "location", "action")
    list_filter = ("location", "action")
