from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'rate', 'views', 'created_at', 'updated_at']
    list_filter = ['rate', 'created_at', 'updated_at']
    search_fields = ['title', 'description']
    readonly_fields = ['views', 'created_at', 'updated_at']
    ordering = ['-created_at']
