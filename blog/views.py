from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import *
from django.core.exceptions import PermissionDenied
from .models import *
from django.urls import *
from .forms import *
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from users.models import *

# Create your views here.

class Home(View):
    def get(self, *args, **kwargs):
        posts = Post.objects.order_by('-posted_date')
        context = {
            'posts':posts
        }
        return render(self.request, 'blog/home.html', context)

class Detail(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        form = CommentForm(request.POST)
        context = {
            'post':post,
            'form':form,
            'comments':comments,
        }
        return render(self.request, 'blog/post.html', context)
    def post(self, request, pk, *rgs, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid:
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(post.get_url())
            else:
                return redirect(post.get_url())


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/addpost.html'
    fields = ('tweet', 'image',)
    login_url = 'user:login'
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post', pk=post.pk)
        form = PostForm()
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/addpost.html', {'form': form})


def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect('blog:home')

    context = {
        'post': post
    }
    return render(request, 'blog/delete.html', context)

def likepost(request):
    #get post to be liked
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    if request.user in post.likes.all():
        #unlike if logged in user has liked
        post.likes.remove(request.user)
    else:
        #like post
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('blog:home'))

def Quote_Post(request, pk):
    parent = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        body = request.POST['body']
        re_tweet, created = Post.objects.get_or_create(
            author=request.user,
            parent=parent,
            retweeted=True,
            tweet=body,
        )
        return redirect('blog:home')
    context = {
        'post':parent,
    }
    return render(request, 'blog/retweet.html', context)

def Retweet(request, pk):
    parent = get_object_or_404(Post, pk=pk)
    re_tweet = Post.objects.create(
        author=request.user,
        parent=parent,
        retweeted=True
    )
    return HttpResponseRedirect(reverse('blog:home'))

def search(request):
    return render(request, 'blog/search.html')

def searchresult(request):
    if request.method =="POST":
        search_info = request.POST['search_info']
        search_type = request.POST['search_type']
        if search_type == "Post":
            result = Post.objects.filter(
                tweet__icontains = search_info
            )
            type = "post"
        if search_type == "User Tag":
            result = UserProfile.objects.filter(
                tag__icontains = search_info
            )
            type = "user"
        context = {
            'result': result,
            'type': type,
            'search': search_info,

        }
        return render(request, 'blog/searchresult.html', context)


