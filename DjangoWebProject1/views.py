from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from datetime import datetime
from .forms import FeedbackForm, CommentForm, BlogForm
from django.contrib.auth.forms import UserCreationForm
from .models import Blog, Comment
from django.contrib.auth.decorators import user_passes_test

def home(request):
    return render(request, 'app/index.html', {
        'title': 'Clothes&Fashion - Главная страница',
        'year': datetime.now().year,
    })

def about(request):
    return render(request, 'app/about.html', {
        'title': 'О магазине Clothes&Fashion',
        'year': datetime.now().year,
    })

def contact(request):
    return render(request, 'app/contact.html', {
        'title': 'Контакты - Clothes&Fashion',
        'year': datetime.now().year,
    })

def catalog(request):
    return render(request, 'app/catalog.html', {
        'title': 'Каталог одежды - Clothes&Fashion',
        'year': datetime.now().year,
    })

def categories(request):
    return render(request, 'app/categories.html', {
        'title': 'Категории одежды - Clothes&Fashion',
        'year': datetime.now().year,
    })

def blogpost(request, parametr):
    try:
        # Получаем текущую статью
        post_1 = get_object_or_404(Blog, id=parametr)
        
        # Получаем ВСЕ статьи для отображения в списке
        posts = Blog.objects.all().order_by('-posted')
        
        # Подсчитываем общее количество комментариев для всех статей
        total_comments = Comment.objects.count()
        
    except Blog.DoesNotExist:
        all_posts = Blog.objects.all()
        return render(request, 'app/blogpost_error.html', {
            'parametr': parametr,
            'available_posts': all_posts,
        })
    
    # Получаем комментарии для текущей статьи
    comments = Comment.objects.filter(post=post_1)
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
            
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.post = post_1
            comment_f.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()

    return render(request, 'app/blogpost.html', {
        'post_1': post_1,
        'posts': posts,  # Все статьи для отображения в списке
        'comments': comments,
        'form': form,
        'total_comments': total_comments,  # Общее количество комментариев
        'title': post_1.title,
        'year': datetime.now().year,
    })

# НОВАЯ ФУНКЦИЯ: Страница со списком всех статей
def blog(request):
    """Страница со списком всех статей блога"""
    posts = Blog.objects.all().order_by('-posted')
    
    return render(request, 'app/blog.html', {
        'posts': posts,
        'title': 'Модный блог - Clothes&Fashion',
        'year': datetime.now().year,
    })

@user_passes_test(lambda u: u.is_superuser)
def newpost(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.posted = datetime.now()
            blog_post.save()
            return redirect('blogpost', parametr=blog_post.id)
    else:
        form = BlogForm()
    
    return render(request, 'app/newpost.html', {
        'form': form,
        'title': 'Добавить статью о моде',
        'year': datetime.now().year,
    })

def videopost(request):
    return render(request, 'app/videopost.html', {
        'title': 'Видео о моде - Clothes&Fashion',
        'year': datetime.now().year,
    })

def feedback(request):
    form = None
    submitted_data = None
    success = False
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            
            submitted_data = {}
            submitted_data['name'] = cleaned_data.get('name', '')
            submitted_data['email'] = cleaned_data.get('email', '')
            
            submitted_data['general_rating'] = cleaned_data.get('general_rating', 'Не указано')
            submitted_data['navigation_rating'] = cleaned_data.get('navigation_rating', 'Не указано')
            submitted_data['recommend'] = cleaned_data.get('recommend', 'Не указано')
            submitted_data['visit_frequency'] = cleaned_data.get('visit_frequency', 'Не указано')
            submitted_data['discovery'] = cleaned_data.get('discovery', 'Не указано')
            
            liked_features = cleaned_data.get('liked_features', [])
            if liked_features:
                submitted_data['liked_features'] = ', '.join(liked_features)
            else:
                submitted_data['liked_features'] = 'Ничего не отмечено'
            
            submitted_data['suggestions'] = cleaned_data.get('suggestions', 'Не указано')
            submitted_data['newsletter'] = 'Да' if cleaned_data.get('newsletter_subscription', False) else 'Нет'
            submitted_data['submission_date'] = datetime.now().strftime("%d.%m.%Y %H:%M")
            
            success = True
    else:
        form = FeedbackForm()
    
    return render(request, 'app/feedback.html', {
        'title': 'Обратная связь - Clothes&Fashion',
        'form': form,
        'submitted_data': submitted_data,
        'success': success,
        'year': datetime.now().year,
    })

def registration(request):
    assert isinstance(request, HttpRequest)
    
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            user = regform.save()
            return redirect('home')
    else:
        regform = UserCreationForm()
    
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,
            'year': datetime.now().year,
            'title': 'Регистрация - Clothes&Fashion'
        }
    )