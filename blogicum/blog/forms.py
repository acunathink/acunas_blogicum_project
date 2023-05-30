from django import forms

from blog.models import Comment, Post


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title', 'text', 'location', 'image', 'pub_date', 'category'
        ]
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%d.%m.%Y %H:%M',
            )
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
