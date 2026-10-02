from django.contrib import admin
from .models import Category, Manufacturer, Medicine, MedicineImage


@admin.register(Category, Manufacturer)
class TaxonomyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class MedicineImageInline(admin.TabularInline):
    model = MedicineImage
    extra = 0


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "generic_name", "category", "manufacturer", "requires_prescription")
    search_fields = ("name", "generic_name")
    list_filter = ("category", "manufacturer", "requires_prescription")
    inlines = (MedicineImageInline,)
