from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, Http404
from blog.models import Comment, Category
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import timezone


class AuthorRequired:

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs[self.pk_url_kwarg]
        instance = get_object_or_404(self.model, pk=pk)
        if instance.author != request.user:
            raise HttpResponseForbidden
        return super().dispatch(request, *args, **kwargs)


class CommentRequired(AuthorRequired):
    model = Comment

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class PaginatePost:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = context['object']
        if 'profile' in context and context['profile'] == self.request.user:
            user_posts = self.object.post_set.all()
        elif type(model) is Category and model.is_published is False:
            raise Http404(f'страница категории "{model}" не существует')
        else:
            user_posts = self.object.post_set.all().filter(
                is_published=True, pub_date__lte=timezone.now()
            )
        paginator = Paginator(user_posts, 10)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        return context
