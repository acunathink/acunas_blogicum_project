from django.shortcuts import get_object_or_404, render

from blog.models import Category, Post

POSTS_LIMIT = 5


def index(request):
    template = 'blog/index.html'

    post_list = Post.public.category().select_related(
        'location', 'author', 'category'
    )[:POSTS_LIMIT]

    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post.public.category(), pk=id)
    context = {'post': post}
    return render(request, template, context)


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
