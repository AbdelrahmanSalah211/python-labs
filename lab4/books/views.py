from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.http import Http404
from django.middleware.csrf import get_token
from django.utils.safestring import mark_safe
from django.contrib import messages
from .models import Book


def book_list(request):
    books = Book.objects.all()
    return TemplateResponse(request, 'books/book_list.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.increment_views()
    return TemplateResponse(request, 'books/book_detail.html', {'book': book})


def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        rate = request.POST.get('rate', 0.00)
        
        if title:
            book = Book.objects.create(
                title=title,
                description=description,
                rate=rate
            )
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'Title is required!')
    
    csrf_token = get_token(request)
    csrf_input = mark_safe(f'<input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">')
    return TemplateResponse(request, 'books/book_form.html', {
        'action': 'Add',
        'csrf_input': csrf_input,
        'book': {}
    })


def book_update(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        rate = request.POST.get('rate', book.rate)
        
        if title:
            book.title = title
            book.description = description
            book.rate = rate
            book.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'Title is required!')
    
    csrf_token = get_token(request)
    csrf_input = mark_safe(f'<input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">')
    return TemplateResponse(request, 'books/book_form.html', {
        'book': book,
        'action': 'Edit',
        'csrf_input': csrf_input
    })


def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book_title = book.title
    book.delete()
    messages.success(request, f'Book "{book_title}" deleted successfully!')
    return redirect('book_list')
