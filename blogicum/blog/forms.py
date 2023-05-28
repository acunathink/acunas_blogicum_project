from django import forms

from blog.models import Post


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title', 'text', 'location', 'image', 'pub_date', 'category'
        ]
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }
