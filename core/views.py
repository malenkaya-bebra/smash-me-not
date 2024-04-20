from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import NewPostForm
from .models import Post, Feed, Notification
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json


class PostListView(ListView):
    model = Post
    template_name = 'core/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            liked_posts = Post.objects.filter(likes__user=self.request.user)
            context['liked_posts'] = liked_posts
        return context


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'core/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(user=user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        liked_posts = Post.objects.filter(user=user, likes__user=self.request.user)
        context['liked_posts'] = liked_posts
        return context


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    is_liked = Like.objects.filter(user=request.user, post=post).exists()
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.username = request.user
            comment.save()
            return redirect('post-detail', pk=pk)
    else:
        form = NewCommentForm()
    return render(request, 'core/post_detail.html', {'post': post, 'is_liked': is_liked, 'form': form})


@login_required
def create_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, f'Posted Successfully')
            return redirect('home')
    else:
        form = NewPostForm()
    return render(request, 'core/create_post.html', {'form': form})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']
    template_name = 'core/create_post.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.user:
        post.delete()
    return redirect('home')


@login_required
def search_posts(request):
    query = request.GET.get('q')
    object_list = Post.objects.filter(content__icontains=query)
    liked_posts = Post.objects.filter(likes__user=request.user)
    return render(request, "core/search_posts.html", {'posts': object_list, 'liked_posts': liked_posts})


@login_required
@require_POST
def like(request):
    post_id = request.POST.get("post_id")
    post = get_object_or_404(Post, pk=post_id)
    liked = False
    like = Like.objects.filter(user=request.user, post=post)
    if like.exists():
        like.delete()
    else:
        liked = True
        Like.objects.create(user=request.user, post=post)
    resp = {'liked': liked}
    return JsonResponse(resp)
