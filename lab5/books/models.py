from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid


def validate_book_title_length(value):
    if len(value) < 10 or len(value) > 50:
        raise ValidationError('Book title must be between 10 and 50 characters.')


def validate_category_name_length(value):
    if len(value) < 2:
        raise ValidationError('Category name must be at least 2 characters.')


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, validators=[validate_category_name_length])
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, validators=[validate_book_title_length])
    description = models.TextField(blank=True)
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    views = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books', null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'book_id': self.pk})
        
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class ISBN(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='isbn')
    author_title = models.CharField(max_length=200)
    book_title = models.CharField(max_length=200)
    isbn_number = models.CharField(max_length=13, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.isbn_number:
            self.isbn_number = str(uuid.uuid4()).replace('-', '')[:13]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"ISBN: {self.isbn_number} - {self.book_title}"