from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from interactions.models import Post, Comment
from users.models import Profile
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone


def home(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        profiles = user_profile.follows.all()
        context["profiles"] = profiles
    return render(request, "home.html", context)


@login_required(login_url="signin")
def create(request):
    if request.method == "POST":
        body = request.POST.get("body")
        post_img = request.FILES.get("post_img")

        if body:
            if post_img:
                new_post = Post.objects.create(
                    author=request.user, body=body, post_img=post_img
                )
            else:
                new_post = Post.objects.create(author=request.user, body=body)
            new_post.save()
            messages.success(request, "Post created successfully")

            return redirect("home")

    return render(request, "create.html")


@login_required(login_url="signin")
def like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.liked_by.add(request.user)
    post.save()
    messages.success(request, "Post liked successfully")

    return redirect("home")


@login_required(login_url="signin")
def unlike(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.liked_by.remove(request.user)
    post.save()

    return redirect("home")


@login_required(login_url="signin")
def unsave(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    post.saved_by.remove(request.user)
    post.save()
    return redirect("saves")


@login_required(login_url="signin")
def save(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    post.saved_by.add(request.user)
    post.save()
    messages.success(request, "Post saved successfully")
    return redirect("saves")


@login_required(login_url="signin")
def saves(request):
    user = request.user
    posts = Post.objects.filter(saved_by=user)
    return render(
        request,
        "save.html",
        {
            "posts": posts,
        },
    )


@login_required(login_url="signin")
def edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        raise PermissionDenied

    if request.method == "POST":
        body = request.POST.get("body")
        post_img = request.FILES.get("post_img")

        if body:
            post.body = body
        if post_img:
            post.post_img = post_img

        post.save()
        messages.success(request, "Post edited successfully")

        return redirect("my_profile")

    return render(request, "edit.html", {"post": post})


@login_required(login_url="signin")
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    messages.success(request, "Post deleted successfully")

    return redirect("my_profile")


@login_required(login_url="signin")
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    text = request.POST.get("text", "")

    if isinstance(request.user, User):
        new_comment = Comment.objects.create(
            author=request.user, post=post, text=text, created_at=timezone.now()
        )
        comments_qs = Comment.objects.filter(post=post).order_by("-created_at")
        new_comment.save()
        comments_list = [
            {
                "text": comment.text,
                "author": comment.author.username,
                "profile_img": comment.author.profile.profile_img.url
                if hasattr(comment.author, "profile")
                and comment.author.profile.profile_img
                else None,
                "created_at": comment.created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),  # Convert to string for JSON
            }
            for comment in comments_qs
        ]

        return JsonResponse({"comments": comments_list}, safe=False)

    else:
        return JsonResponse({"success": False, "error": "Invalid user instance"})


def comments(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments_qs = Comment.objects.filter(post=post).order_by("-created_at")

    comments_list = [
        {
            "text": comment.text,
            "author": comment.author.username,
            "profile_img": comment.author.profile.profile_img.url
            if hasattr(comment.author, "profile") and comment.author.profile.profile_img
            else None,
            "created_at": comment.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),  # Convert to string for JSON
        }
        for comment in comments_qs
    ]

    if request.method == "POST":
        return create_comment(request, post_id)

    return JsonResponse({"comments": comments_list}, safe=False)


def search(request):

    if request.method == "POST":
        username = request.POST.get("username")
        profiles = Profile.objects.filter(user__username__icontains=username)

        if not profiles.exists():
            messages.error(request, "No profiles found for the given username.")

        return render(
            request, "search.html", {"profiles": profiles, "search_term": username}
        )
    return render(request, "search.html")


@login_required(login_url="signin")
def follow(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.user.profile != profile:
        request.user.profile.follows.add(profile)
        messages.success(request, "You are followed successfully")

    return JsonResponse({"status": "success"})


@login_required(login_url="signin")
def unfollow(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.user.profile != profile:
        request.user.profile.follows.remove(profile)
        messages.success(request, "You have unfollowed successfully")

    return JsonResponse({"status": "success"})


def get_followers_count(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    return JsonResponse({"followers_count": profile.followers.count()}, safe=False)
