from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.middleware.csrf import get_token


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    
    csrf_token = get_token(request)
    csrf_input = mark_safe(f'<input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">')
    return render(request, 'accounts/signup.html', {
        'form': form, 
        'csrf_input': csrf_input,
        'user': request.user
    })


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('book_list')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('book_list')
