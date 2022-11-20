from django.db import models
from django.conf import settings
from django.utils import timezone
import random, string
from django.shortcuts import reverse
# Create your models here.

#create ref code
def post_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def comment_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tweet = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name='parenttweet', null=True, blank=True)
    post_code =models.CharField(max_length=20, default=post_code())
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="post_likes")
    posted_date = models.DateTimeField(default=timezone.now)

    def retweet(self):
        return reverse("blog:retweet_post", kwargs={
            'pk': self.pk,
        })

    def total_likes(self):
        return self.likes.count()

    def get_url(self):
        return reverse("blog:post", kwargs={
            'pk': self.pk,
            'ref':self.post_code
        })

    def edit_url(self):
        return reverse("blog:edit_post", kwargs={
            'pk': self.pk,
        })

    def delete_url(self):
        return reverse("blog:delete_post", kwargs={
            'pk': self.pk,
        })

    def __str__(self):
        return f"{self.author} post {self.pk}"


class Comment(models.Model):
    post = models.ForeignKey('Post', related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_code = models.CharField(max_length=100, default=comment_code())
    comment_date = models.DateField(default=timezone.now)


    def __str__(self):
        return f"comment {self.pk} on post {self.post.pk}"

class Reply(models.Model):
    comment = models.ForeignKey('Comment', related_name="reply", on_delete=models.CASCADE)
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reply = models.TextField()
    reply_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"comment {self.pk} on comment {self.comment.pk}"

