from django.db import models
from django.db.models import Count
from django.utils import timezone


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
            pub_date__lte=timezone.now()
        )


class CategoryManager(PublishManager):
    def category(self):
        return (
            self.filter(category__is_published=True)
            .annotate(comment_count=Count('comments'))
        )
