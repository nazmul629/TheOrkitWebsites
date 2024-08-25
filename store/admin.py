from django.contrib import admin
from .models import Product, Variation, ReviewRating,ProductGallery
import admin_thumbnails



@admin_thumbnails.thumbnail('image')
class ProductGallleryInline(admin.TabularInline):
    model =ProductGallery
    extra = 1 

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug':('product_name',)}
    inlines =[ProductGallleryInline]

    list_display= ('product_name','category','stock','price','is_avilable',)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category')

    

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)

admin.site.register(ReviewRating)
admin.site.register(ProductGallery)