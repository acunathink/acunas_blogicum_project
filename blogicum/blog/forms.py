from django import forms
from django.utils import timezone

from blog.models import Comment, Post


class PostCreateForm(forms.ModelForm):
    pub_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now().strftime('%Y-%m-%d %H:%M')
    )

    class Meta:
        model = Post
        fields = [
            'title', 'text', 'location', 'image', 'pub_date', 'category'
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
