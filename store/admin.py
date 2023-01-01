from django.contrib import admin
from .models import Category, Product, Customer, Orders
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display= ['name', 'slug' ]
    prepopulated_fields = {'slug' : ('name',)}
    
   
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description', 'image','price', 'slug']

    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Customer)

admin.site.register(Orders)