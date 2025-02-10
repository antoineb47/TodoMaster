from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Todo
from django.db.models import Q

@login_required
def todo_list(request):
    filter_status = request.GET.get('status', 'all')
    filter_priority = request.GET.get('priority', 'all')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-created_at')

    todos = Todo.objects.filter(user=request.user)

    if search_query:
        todos = todos.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(tags__icontains=search_query)
        )

    if filter_status == 'completed':
        todos = todos.filter(completed=True)
    elif filter_status == 'active':
        todos = todos.filter(completed=False)
    elif filter_status == 'overdue':
        todos = todos.filter(due_date__lt=timezone.now(), completed=False)

    if filter_priority != 'all':
        todos = todos.filter(priority=filter_priority)

    # Apply sorting
    if sort_by == 'due_date':
        todos = todos.order_by('due_date', '-created_at')
    elif sort_by == 'priority':
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        todos = sorted(todos, key=lambda x: (priority_order[x.priority], -x.created_at.timestamp()))
    elif sort_by == 'title':
        todos = todos.order_by('title', '-created_at')
    else:  # default to created_at
        todos = todos.order_by('-created_at')

    # Calculate statistics
    total_count = todos.count()
    completed_count = todos.filter(completed=True).count()
    completed_percentage = (completed_count / total_count * 100) if total_count > 0 else 0
    high_priority_count = todos.filter(priority='high').count()
    
    # Calculate due soon (tasks due within next 24 hours)
    now = timezone.now()
    tomorrow = now + timezone.timedelta(days=1)
    due_soon_count = todos.filter(
        due_date__isnull=False,
        due_date__range=(now, tomorrow),
        completed=False
    ).count()

    context = {
        'todos': todos,
        'filter_status': filter_status,
        'filter_priority': filter_priority,
        'search_query': search_query,
        'completed_count': completed_count,
        'completed_percentage': completed_percentage,
        'high_priority_count': high_priority_count,
        'due_soon_count': due_soon_count
    }
    return render(request, 'todos/todo_list.html', context)

@login_required
def todo_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        category = request.POST.get('category')
        tags = request.POST.get('tags')
        due_date_str = request.POST.get('due_date')
        
        try:
            due_date = timezone.datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M') if due_date_str else None
            Todo.objects.create(
                title=title,
                description=description,
                priority=priority,
                category=category,
                tags=tags,
                due_date=due_date,
                user=request.user
            )
            messages.success(request, 'Task created successfully!')
            return redirect('todo_list')
        except Exception as e:
            messages.error(request, f'Error creating task: {str(e)}')
            
    return render(request, 'todos/todo_create.html')

@login_required
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.priority = request.POST.get('priority')
        todo.category = request.POST.get('category')
        todo.tags = request.POST.get('tags')
        due_date_str = request.POST.get('due_date')
        todo.completed = request.POST.get('completed') == 'on'
        
        try:
            todo.due_date = timezone.datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M') if due_date_str else None
            todo.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('todo_list')
        except Exception as e:
            messages.error(request, f'Error updating task: {str(e)}')
            
    return render(request, 'todos/todo_update.html', {'todo': todo})

@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('todo_list')

@login_required
def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')
