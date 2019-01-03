from django.contrib import admin

# Register your models here.
from . models import Product,ProductFile


class ProductFileInLine(admin.TabularInline):
    model = ProductFile
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__','slug','is_digital']
    inlines = [ProductFileInLine]
    class Meta:
        model=Product


admin.site.register(Product, ProductAdmin)
