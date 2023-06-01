from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, View

from blog.constants import POSTS_PER_PAGE
from blog.models import Comment, User


class AuthorRequiredMixin(View):

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs[self.pk_url_kwarg]
        instance = get_object_or_404(self.model, pk=pk)
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=pk)
        return super().dispatch(request, *args, **kwargs)


class CommentMixin(AuthorRequiredMixin):
    model = Comment
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class PostSetMixin(DetailView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if isinstance(self.object, User) and self.object == request.user:
            post_set = self.object.post_set.all()
        else:
            post_set = (
                self.object.post_set.all()
                .filter(is_published=True, pub_date__lte=timezone.now())
            )

        self.kwargs['post_set'] = (
            post_set.order_by('-pub_date')
            .annotate(comment_count=Count('comments'))
        )

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PaginateMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_set = self.kwargs['post_set']
        paginator = Paginator(post_set, POSTS_PER_PAGE)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        return context
