from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Book, Category
from django.db import transaction


class Command(BaseCommand):
    help = 'Populate the database with sample books and categories'

    @transaction.atomic
    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@test.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f"Created user: {user.username}")
        
        categories_data = [
            ('Fiction', 'Fictional stories and novels'),
            ('Science', 'Science and technology books'),
            ('History', 'Historical books and documentaries'),
            ('Biography', 'Life stories of famous people'),
            ('Technology', 'Programming and technical books'),
        ]
        
        for name, description in categories_data:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(f"Created category: {category.name}")
        
        books_data = [
            ('The Great Adventure Story', 'An amazing adventure through unknown lands and mysterious places', 4.5, ['Fiction']),
            ('Python Programming Guide', 'Complete guide to Python programming and web development', 4.8, ['Technology']),
            ('World History Chronicles', 'Comprehensive history of the world and its civilizations', 4.2, ['History']),
            ('Life of Einstein Biography', 'Biography of the famous physicist Albert Einstein', 4.7, ['Biography', 'Science']),
            ('Django Web Development', 'Modern web development with Django framework and Python', 4.6, ['Technology']),
        ]
        
        for title, description, rate, category_names in books_data:
            book, created = Book.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'rate': rate,
                    'user': user
                }
            )
            if created:
                for cat_name in category_names:
                    category = Category.objects.get(name=cat_name)
                    book.categories.add(category)
                self.stdout.write(f"Created book: {book.title}")

        self.stdout.write(self.style.SUCCESS('Sample data populated successfully!'))
