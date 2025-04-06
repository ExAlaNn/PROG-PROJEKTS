from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
from .models import Todo
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserChangeForm
from django.http import JsonResponse
from datetime import datetime

@login_required
def admin_dashboard(request):
    if not request.user.profile.role == 'admin':
        return redirect('todos')
    return render(request, 'admin_dashboard.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.profile.role = 'user'  
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')  

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('todos')  
        else:
            messages.error(request, 'Wrong password')  
            return redirect('login') 
    return render(request, 'login.html')

def logout_view(request):
    logout(request)  
    return redirect('login')  

@login_required
def todos(request):
    category_filter = request.GET.get('category')  
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            if not todo.category:  
                messages.error(request, 'Please select a category')  
            else:
                todo.user = request.user  
                todo.save()
                return redirect('todos')
    else:
        form = TodoForm()

    
    unfinished_todos = Todo.objects.filter(user=request.user, is_done=False)
    if category_filter:  
        unfinished_todos = unfinished_todos.filter(category__id=category_filter)
    finished_todos = Todo.objects.filter(user=request.user, is_done=True)
    return render(request, 'todos.html', {
        'unfinished_todos': unfinished_todos,
        'finished_todos': finished_todos,
        'form': form,
        'category_filter': category_filter, 
    })

@login_required
def mark_done(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)  
    todo.is_done = True
    todo.save()
    messages.success(request, f'Task "{todo.title}" marked as done!')
    return redirect('todos')

@login_required
def edit_task(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('todos')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'edit_task.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

@login_required
def update_task_date(request, todo_id):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        new_date = request.POST.get('date')
        try:
            todo.date_added = datetime.strptime(new_date, '%Y-%m-%d')
            todo.save()
            return JsonResponse({'success': True})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid date format'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def delete_finished_tasks(request):
    Todo.objects.filter(user=request.user, is_done=True).delete()
    messages.success(request, 'All finished tasks have been deleted!')
    return redirect('todos')