from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('preview','title', 'price', 'is_published', 'quantity')
    list_editable = ('is_published','quantity')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('preview',)

    def preview(self, obj):
        return mark_safe(f"<img src = '{obj.get_preview()}' width=100 >")