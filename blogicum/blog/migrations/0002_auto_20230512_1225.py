# Generated by Django 3.2.16 on 2023-05-12 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'локация', 'verbose_name_plural': 'Локации'},
        ),
        migrations.AddField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(null=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='location',
            name='title',
            field=models.CharField(help_text='Географическая метка', max_length=256, verbose_name='Локация'),
        ),
    ]
