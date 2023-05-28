from django.contrib import admin

from blog.models import Category, Location, Post

admin.site.register(Category)
admin.site.register(Location)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
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
    list_filter = ('category',)


admin.site.register(Post, PostAdmin)
