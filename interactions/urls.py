from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("like/<int:post_id>/", views.like, name="like"),
    path("unlike/<int:post_id>/", views.unlike, name="unlike"),
    path("unsave/<int:post_id>/", views.unsave, name="unsave"),
    path("save/<int:post_id>/", views.save, name="save"),
    path("saves/", views.saves, name="saves"),
    path("edit/<int:post_id>/", views.edit, name="edit"),
    path("delete/<int:post_id>/", views.delete, name="delete_post"),
    path('comments/<int:post_id>/', views.comments, name='comments'),
    path('comments/create/<int:post_id>/', views.create_comment, name='create_comment'),
    path("search/", views.search, name="search"),
    path("follow/<int:profile_id>/", views.follow, name="follow"),
    path("unfollow/<int:profile_id>/", views.unfollow, name="unfollow"),
    path("get/followers-count/<int:profile_id>/", views.get_followers_count, name="get_followers_count"),
]