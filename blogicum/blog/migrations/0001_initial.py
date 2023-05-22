# Generated by Django 3.2.16 on 2023-05-12 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название категории')),
                ('description', models.TextField(verbose_name='Описание')),
                ('slug', models.SlugField(max_length=64, unique=True, verbose_name='Слаг')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публиковать')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Уникальное название обёртки, не более 256 символов', max_length=256, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'обёртка',
                'verbose_name_plural': 'Обёртки',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('text', models.TextField(verbose_name='текст публикации')),
                ('pub_date', models.DateTimeField(verbose_name='дата публикации')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публиковать')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата написания')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category', verbose_name='Категория')),
                ('location', models.ForeignKey(blank=True, default='Планета Земля', null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.location', verbose_name='Географическая метка')),
            ],
            options={
                'verbose_name': 'Публикация',
                'verbose_name_plural': 'Посты',
                'ordering': ('created_at', 'pub_date', 'title'),
            },
        ),
    ]
