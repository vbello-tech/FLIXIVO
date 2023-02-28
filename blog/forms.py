from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    "placeholder": 'Enter your comment here',
                    'rows': 10,
                    'cols': 80,
                }
            )

        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('tweet', 'image',)


        widgets = {
            'tweet': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 10,
                    'cols': 80,
                    'placeholder':"TYPE YOUR TWEET.",
                }
            )

        }



