from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book, ISBN


@receiver(post_save, sender=Book)
def create_isbn_for_book(sender, instance, created, **kwargs):
    """
    Signal to create ISBN object when a book is created
    """
    if created:
        ISBN.objects.create(
            book=instance,
            author_title=f"Author of {instance.title}",
            book_title=instance.title
        )
