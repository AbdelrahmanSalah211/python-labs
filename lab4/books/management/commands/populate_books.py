from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    help = 'Populate the database with sample books'

    def handle(self, *args, **options):
        Book.objects.all().delete()
        books = [
            {
                'title': 'The Great Gatsby',
                'description': 'A classic American novel written by F. Scott Fitzgerald, published in 1925. Set in the Jazz Age on Long Island, it tells the story of Jay Gatsby and his pursuit of the American Dream.',
                'rate': 4.5,
            },
            {
                'title': '1984',
                'description': 'A dystopian social science fiction novel by George Orwell, published in 1949. It explores themes of totalitarianism, surveillance, and the loss of individual freedom.',
                'rate': 4.8,
            },
            {
                'title': 'To Kill a Mockingbird',
                'description': 'A novel by Harper Lee published in 1960, exploring racial injustice in the Deep South through the eyes of Scout Finch, a young girl growing up in Alabama.',
                'rate': 4.6,
            },
            {
                'title': 'Pride and Prejudice',
                'description': 'A romantic novel by Jane Austen, first published in 1813. It follows the main character Elizabeth Bennet as she deals with issues of manners, upbringing, morality, and marriage.',
                'rate': 4.3,
            },
            {
                'title': 'The Catcher in the Rye',
                'description': 'A novel by J.D. Salinger, published in 1951. It follows Holden Caulfield, a teenager from New York City, as he navigates the challenges of adolescence and society.',
                'rate': 4.0,
            },
        ]
        
        for book_data in books:
            book = Book.objects.create(**book_data)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created book: {book.title}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully populated database with {len(books)} books')
        )
