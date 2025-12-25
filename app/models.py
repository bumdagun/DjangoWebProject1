from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime

class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Заголовок статьи")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Опубликована")
    
    image = models.FileField(
        default='temp.jpg',
        verbose_name='Путь к картинке',
        upload_to='blog_images/'
    )
    
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField(
        verbose_name="Текст комментария",
        help_text="Напишите ваш комментарий"
    )
    
    date = models.DateTimeField(
        default=datetime.now,
        db_index=True,
        verbose_name="Дата добавления"
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария"
    )
    
    post = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Статья блога"
    )
    
    class Meta:
        db_table = "Comments"
        ordering = ["-date"]  
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
    
    def __str__(self):
        return f"Комментарий {self.author} к {self.post.title}"