from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from blog import forms, mixins
from blog.models import Category, Post, User


class PostListView(ListView):
    model = Post
    queryset = Post.public.category().select_related(
        'category', 'location', 'author'
    )
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    paginate_by = mixins.POSTS_PER_PAGE


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = forms.PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.success_url = reverse(
            'blog:profile', kwargs={'username': self.request.user}
        )
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostUpdateView(LoginRequiredMixin, mixins.AuthorRequired, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = forms.PostCreateForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs['pk']}
        )


class PostDeleteView(LoginRequiredMixin, mixins.AuthorRequired, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'pk'


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = forms.CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


class CommentEdit(LoginRequiredMixin, mixins.CommentRequired, UpdateView):
    template_name = 'blog/comment.html'
    fields = ['text', ]


class CommentDelete(LoginRequiredMixin, mixins.CommentRequired, DeleteView):
    template_name = 'blog/comment.html'


class CategoryDetailView(mixins.PostFilter, mixins.PaginatePost, DetailView):
    model = Category
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'category'

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)
        return queryset


class UserDetailView(mixins.PostFilter, mixins.PaginatePost, DetailView):
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ['first_name', 'last_name', 'username', 'email']
    success_url = reverse_lazy('blog:index')
