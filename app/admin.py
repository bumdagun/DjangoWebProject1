from django.contrib import admin
from .models import Blog, Comment

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted', 'description_short')
    list_display_links = ('title',)
    search_fields = ('title', 'description', 'content')
    list_filter = ('posted',)
    
    fields = ('title', 'description', 'content', 'posted', 'image')
    
    def description_short(self, obj):
        if len(obj.description) > 50:
            return obj.description[:50] + '...'
        return obj.description
    description_short.short_description = 'Краткое содержание'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'date', 'text_short')
    list_display_links = ('author', 'post')
    search_fields = ('text', 'author__username', 'post__title')
    list_filter = ('date', 'author', 'post')
    
    fields = ('post', 'author', 'text', 'date')
    readonly_fields = ('date',)
    
    def text_short(self, obj):
        if len(obj.text) > 50:
            return obj.text[:50] + '...'
        return obj.text
    text_short.short_description = 'Текст комментария'
    
    def save_model(self, request, obj, form, change):
        if not change:
            if not obj.author_id:
                obj.author = request.user
        super().save_model(request, obj, form, change)
