from django.contrib import admin
from .models import Book, Category, ISBN


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


class ISBNInline(admin.StackedInline):
    model = ISBN
    extra = 0
    readonly_fields = ['isbn_number', 'created_at']
    max_num = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'rate', 'views', 'created_at', 'updated_at']
    list_filter = ['rate', 'user', 'categories', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['views', 'created_at', 'updated_at']
    ordering = ['-created_at']
    filter_horizontal = ['categories']
    inlines = [ISBNInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').prefetch_related('categories')


@admin.register(ISBN)
class ISBNAdmin(admin.ModelAdmin):
    list_display = ['isbn_number', 'book_title', 'author_title', 'book', 'created_at']
    list_filter = ['created_at']
    search_fields = ['isbn_number', 'book_title', 'author_title', 'book__title']
    readonly_fields = ['isbn_number', 'created_at']
    ordering = ['-created_at']
