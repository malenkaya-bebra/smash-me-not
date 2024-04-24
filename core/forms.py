from django import forms
from .models import Comment, Post


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'tags', 'feed']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'feed': forms.Select(attrs={'class': 'form-control'}),
        }


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
