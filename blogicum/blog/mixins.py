from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from blog.models import Comment

POSTS_PER_PAGE = 10


class AuthorRequired:

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs[self.pk_url_kwarg]
        instance = get_object_or_404(self.model, pk=pk)
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=pk)
        return super().dispatch(request, *args, **kwargs)


class CommentRequired(AuthorRequired):
    model = Comment
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class PostFilter:

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object == request.user):
            user_posts = (
                self.object.post_set.all()
                .order_by('-pub_date')
                .annotate(comment_count=Count('comments'))
            )
        else:
            user_posts = (
                self.object.post_set.all()
                .filter(is_published=True, pub_date__lte=timezone.now())
                .order_by('-pub_date')
                .annotate(comment_count=Count('comments'))
            )
        self.kwargs['user_posts'] = user_posts
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PaginatePost:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_posts = self.kwargs['user_posts']
        paginator = Paginator(user_posts, POSTS_PER_PAGE)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        return context
