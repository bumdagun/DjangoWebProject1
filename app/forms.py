from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator
from .models import Blog

class FeedbackForm(forms.Form):
    # Текстовые поля
    name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        min_length=2,
        validators=[
            MinLengthValidator(2, "Имя должно содержать минимум 2 символа"),
            MaxLengthValidator(100, "Имя не должно превышать 100 символов")
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        }),
        required=True
    )
    
    email = forms.EmailField(
        label='Email',
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.ru'
        }),
        required=True
    )
    
    # Радиокнопки
    general_rating = forms.ChoiceField(
        label='Общая оценка сайта',
        choices=[
            ('5', 'Отлично'),
            ('4', 'Хорошо'),
            ('3', 'Удовлетворительно'),
            ('2', 'Плохо'),
            ('1', 'Очень плохо'),
        ],
        widget=forms.RadioSelect(),
        required=True,
        initial='5'
    )
    
    navigation_rating = forms.ChoiceField(
        label='Удобство навигации по сайту',
        choices=[
            ('5', 'Очень удобно'),
            ('4', 'Удобно'),
            ('3', 'Нормально'),
            ('2', 'Неудобно'),
            ('1', 'Очень неудобно'),
        ],
        widget=forms.RadioSelect(),
        required=True,
        initial='5'
    )
    
    recommend = forms.ChoiceField(
        label='Рекомендуете ли вы наш сайт друзьям?',
        choices=[
            ('yes', 'Да, обязательно'),
            ('maybe', 'Возможно'),
            ('no', 'Нет'),
        ],
        widget=forms.RadioSelect(),
        required=True,
        initial='yes'
    )
    
    # ВЫПАДАЮЩИЕ СПИСКИ - ИСПРАВЛЕННЫЕ БЕЗ ДУБЛИКАТОВ
    visit_frequency = forms.ChoiceField(
        label='Как часто вы посещаете наш сайт?',
        choices=[
            ('daily', 'Ежедневно'),
            ('weekly', 'Несколько раз в неделю'),
            ('monthly', 'Несколько раз в месяц'),
            ('rarely', 'Редко'),
            ('first', 'Впервые на сайте'),
        ],
        widget=forms.RadioSelect(),  # Изменено с Select на RadioSelect
        required=True,
        initial='monthly'
    )
    
    discovery = forms.ChoiceField(
        label='Как вы узнали о нашем сайте?',
        choices=[
            ('search', 'Из поисковой системы (Google, Yandex)'),
            ('social', 'Из социальных сетей'),
            ('friend', 'От друзей/знакомых'),
            ('ad', 'Реклама'),
            ('other', 'Другое'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        initial='search'
    )
    
    # Множественный выбор (флажки)
    liked_features = forms.MultipleChoiceField(
        label='Что вам понравилось на сайте? (можно выбрать несколько вариантов)',
        choices=[
            ('design', 'Дизайн сайта'),
            ('navigation', 'Удобство навигации'),
            ('content', 'Содержание статей и блога'),
            ('catalog', 'Каталог товаров'),
            ('support', 'Поддержка клиентов'),
            ('prices', 'Цены и акции'),
            ('speed', 'Скорость работы сайта'),
        ],
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        help_text='Отметьте все подходящие варианты'
    )
    
    # Текстовое поле
    suggestions = forms.CharField(
        label='Ваши предложения по улучшению сайта',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Оставьте ваши пожелания и предложения...',
            'rows': 4
        }),
        required=False,
        help_text='Ваши идеи помогут нам стать лучше'
    )
    
    # Флажки (чекбоксы)
    newsletter_subscription = forms.BooleanField(
        label='Хочу получать новости, акции и специальные предложения на email',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        initial=False
    )
    
    privacy_agreement = forms.BooleanField(
        label='Я согласен на обработку моих персональных данных в соответствии с политикой конфиденциальности',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': 'Вы должны согласиться на обработку персональных данных'}
    )

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите краткое содержание',
                'rows': 3
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите полное содержание',
                'rows': 10
            }),
        }