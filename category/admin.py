# category/admin.py

from django.contrib import admin
from .models import Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)} # Recommend Slug field based on category_name
    list_display = ('category_name', 'slug')
    
admin.site.register(Category, CategoryAdmin)
