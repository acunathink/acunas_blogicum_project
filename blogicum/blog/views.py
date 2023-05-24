from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from blog.models import Category, Post
from blog.mixins import AuthorRequiredMixin


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    paginate_by = 10


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'


class UserBaseUpdateView(UpdateView):
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


class PostUpdateView(AuthorRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'text', 'location', 'image', 'pub_date', 'category']
    success_url = reverse_lazy('blog:index')


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.published.select_related(
        'location', 'author', 'category'
    ).filter(category=category)

    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)
