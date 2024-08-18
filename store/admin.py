from django.contrib import admin
from .models import Product, Variation


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug':('product_name',)}

    list_display= ('product_name','category','stock','price','is_avilable',)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category')

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)