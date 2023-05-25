from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from blog.models import Category, Post, CommentForm, Comment
from blog import mixins


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    paginate_by = 10


class UserDetailView(mixins.PaginatePost, DetailView):
    model = get_user_model()
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'


class CategoryDetailView(mixins.PaginatePost, DetailView):
    model = Category
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'category'


class UserUpdateView(UpdateView):
    model = get_user_model()
    template_name = 'blog/user.html'
    fields = ['first_name', 'last_name', 'username', 'email']
    success_url = reverse_lazy('blog:index')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text', 'location', 'image', 'pub_date', 'category']
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostUpdateView(LoginRequiredMixin, mixins.AuthorRequired, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'text', 'location', 'image', 'pub_date', 'category']
    success_url = reverse_lazy('blog:index')


class PostDeleteView(LoginRequiredMixin, mixins.AuthorRequired, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'pk'


@login_required
def edit_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        print(f'|| pk >{pk}< ||')
    return redirect('blog:post_detail', pk=pk)


class СommentCreateView(LoginRequiredMixin, CreateView):
    comment = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.comment = self.comment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post.pk})


class CommentEdit(LoginRequiredMixin, mixins.CommentRequired, UpdateView):
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    fields = ['text', ]


class CommentDelete(LoginRequiredMixin, mixins.CommentRequired, DeleteView):
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
