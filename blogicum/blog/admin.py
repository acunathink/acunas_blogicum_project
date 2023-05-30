from django.contrib import admin

from blog.models import Category, Location, Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'count_comms',
        'author',
        'category',
        'pub_date',
        'is_published'
    )
    list_editable = (
        'is_published',
        'pub_date',
        'category'
    )
    search_fields = ('title', )
    list_filter = ('category', 'author')

    @admin.display(description='К-во комментариев')
    def count_comms(self, obj):
        return obj.comments.count()


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'created_at', 'author', 'text', 'post'
    )
    list_filter = ('author', 'post')


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Comment, CommentAdmin)
