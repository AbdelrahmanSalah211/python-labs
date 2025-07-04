from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.http import Http404
from django.middleware.csrf import get_token
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from .models import Book, Category


def book_list(request):
    books = Book.objects.select_related('user').prefetch_related('categories')
    return TemplateResponse(request, 'books/book_list.html', {
        'books': books,
        'user': request.user
    })


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.increment_views()
    return TemplateResponse(request, 'books/book_detail.html', {
        'book': book,
        'user': request.user
    })


@login_required
def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        rate = request.POST.get('rate', 0.00)
        category_ids = request.POST.getlist('categories')
        
        if title:
            try:
                book = Book(
                    title=title,
                    description=description,
                    rate=rate,
                    user=request.user
                )
                book.full_clean()
                book.save()
                
                if category_ids:
                    book.categories.set(category_ids)
                
                messages.success(request, f'Book "{book.title}" created successfully!')
                return redirect('book_list')
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        else:
            messages.error(request, 'Title is required!')
    
    categories = Category.objects.all()
    csrf_token = get_token(request)
    csrf_input = mark_safe(f'<input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">')
    return TemplateResponse(request, 'books/book_form.html', {
        'action': 'Add',
        'csrf_input': csrf_input,
        'book': {},
        'categories': categories,
        'user': request.user
    })


@permission_required('books.change_book', raise_exception=True)
def book_update(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        rate = request.POST.get('rate', book.rate)
        category_ids = request.POST.getlist('categories')
        
        if title:
            try:
                book.title = title
                book.description = description
                book.rate = rate
                book.full_clean()
                book.save()
                
                if category_ids:
                    book.categories.set(category_ids)
                else:
                    book.categories.clear()
                
                messages.success(request, f'Book "{book.title}" updated successfully!')
                return redirect('book_list')
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        else:
            messages.error(request, 'Title is required!')
    
    categories = Category.objects.all()
    csrf_token = get_token(request)
    csrf_input = mark_safe(f'<input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">')
    return TemplateResponse(request, 'books/book_form.html', {
        'book': book,
        'action': 'Edit',
        'csrf_input': csrf_input,
        'categories': categories,
        'user': request.user
    })


@permission_required('books.delete_book', raise_exception=True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book_title = book.title
    book.delete()
    messages.success(request, f'Book "{book_title}" deleted successfully!')
    return redirect('book_list')
