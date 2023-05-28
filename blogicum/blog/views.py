from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from blog import forms, mixins
from blog.models import Category, CommentForm, Post


class PostListView(ListView):
    model = Post
    queryset = Post.public.category()
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    paginate_by = 10


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = forms.PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.success_url = reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user}
        )
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
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


class CommentEdit(LoginRequiredMixin, mixins.CommentRequired, UpdateView):
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    fields = ['text', ]


class CommentDelete(LoginRequiredMixin, mixins.CommentRequired, DeleteView):
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class CategoryDetailView(mixins.PaginatePost, DetailView):
    model = Category
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'category'


class UserDetailView(mixins.PaginatePost, DetailView):
    model = get_user_model()
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'blog/user.html'
    fields = ['first_name', 'last_name', 'username', 'email']
    success_url = reverse_lazy('blog:index')
