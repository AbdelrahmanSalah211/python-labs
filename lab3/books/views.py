from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.http import Http404

BOOKS = [
    {'id': 1, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'description': 'A classic novel set in the Jazz Age.'},
    {'id': 2, 'title': '1984', 'author': 'George Orwell', 'description': 'A dystopian novel about totalitarianism.'},
    {'id': 3, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'description': 'A novel about racial injustice in the Deep South.'},
]


def get_book(book_id):
    return next((book for book in BOOKS if book['id'] == book_id), None)


def book_list(request):
    return TemplateResponse(request, 'books/book_list.html', {'books': BOOKS})


def book_detail(request, book_id):
    book = get_book(book_id)
    if not book:
        raise Http404('Book not found')
    return TemplateResponse(request, 'books/book_detail.html', {'book': book})


def book_create(request):
    if request.method == 'POST':
        new_id = max(book['id'] for book in BOOKS) + 1 if BOOKS else 1
        BOOKS.append({
            'id': new_id,
            'title': request.POST['title'],
            'author': request.POST['author'],
            'description': request.POST['description'],
        })
        return redirect('book_list')
    return TemplateResponse(request, 'books/book_form.html', {'action': 'Add'})


def book_update(request, book_id):
    book = get_book(book_id)
    if not book:
        return redirect('book_list')
    if request.method == 'POST':
        book['title'] = request.POST['title']
        book['author'] = request.POST['author']
        book['description'] = request.POST['description']
        return redirect('book_list')
    return TemplateResponse(request, 'books/book_form.html', {'book': book, 'action': 'Edit'})


def book_delete(request, book_id):
    global BOOKS
    BOOKS = [book for book in BOOKS if book['id'] != book_id]
    return redirect('book_list')
