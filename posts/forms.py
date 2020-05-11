from .models import Comment,Post
from django import forms
from tinymce.widgets import TinyMCE


class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'id': 'usercomment', 'placeholder': 'Type your comment', 'class': 'form-control', 'rows':'4' }))
    class Meta:
        model = Comment
        fields = ('comment',)


class PostForm(forms.ModelForm):
    
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    
    class Meta:
        model = Post
        fields = ("title","overview","content","thumbnail","categories","featured","previous_post","next_post",)