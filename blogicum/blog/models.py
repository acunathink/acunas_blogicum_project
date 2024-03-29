from django.contrib.auth import get_user_model
from django.db import models

from blog import managers

User = get_user_model()


class BaseModel(models.Model):
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        default=True
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class TitleModel(models.Model):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField(
        verbose_name='Название места',
        max_length=256,
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(BaseModel, TitleModel):
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ),
        max_length=64,
        unique=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Post(BaseModel, TitleModel):
    text = models.TextField(
        verbose_name='Текст'
    )
    image = models.ImageField(
        'Изображение', upload_to='posts_images', blank=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
    )

    objects = models.Manager()
    public = managers.CategoryManager()
    published = managers.PublishManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', '-created_at', 'title')


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
