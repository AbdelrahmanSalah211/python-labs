from django.db import models
from django.urls import reverse

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    views = models.PositiveIntegerField(default=0)
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