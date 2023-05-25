from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from blog.models import Comment
from django.urls import reverse
from django.core.paginator import Paginator


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
        user_posts = self.object.post_set.all()
        paginator = Paginator(user_posts, 10)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        return context
