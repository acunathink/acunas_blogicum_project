from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from blog.models import Post


class AuthorRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        # При получении объекта не указываем автора.
        # Результат сохраняем в переменную.
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        # Сверяем автора объекта и пользователя из запроса.
        if instance.author != request.user:
            # Здесь может быть как вызов ошибки,
            # так и редирект на нужную страницу.
            raise HttpResponseForbidden
        return super().dispatch(request, *args, **kwargs)
