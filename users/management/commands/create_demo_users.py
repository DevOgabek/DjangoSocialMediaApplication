from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile
from interactions.models import Post, Comment

class Command(BaseCommand):
    help = 'Creates 300 users with profiles and interacts with "DevOgabek" user'
    
    def handle(self, *args, **kwargs):
        devogabek_user = User.objects.get(username='DevOgabek')

        for i in range(1, 301):  
            username = f"user_{i}"
            email = f"user{i}@example.com"
            password = f"user_{i}_password"
            user = User.objects.create_user(username=username, email=email, password=password)

            profile = Profile.objects.create(
                user=user,
                first_name=f"First_{i}",
                last_name=f"Last_{i}",
            )
            profile.follows.add(devogabek_user.profile)
            profile.save()

            self.stdout.write(self.style.SUCCESS(f"Created user and profile: {username}"))

            sogabekavazov_posts = Post.objects.filter(author=devogabek_user)
            for post in sogabekavazov_posts:
                post.liked_by.add(user)
                self.stdout.write(self.style.SUCCESS(f"User {username} liked post by 'DevOgabek'"))

            if i % 25 == 0:
                for post in sogabekavazov_posts:
                    Comment.objects.create(post=post, author=user, text=f"Comment by {user.username} on post by {post.author.username}")
                    self.stdout.write(self.style.SUCCESS(f"User {username} added a comment on post by 'DevOgabek'"))

        self.stdout.write(self.style.SUCCESS(f"All users and profiles now follow 'DevOgabek', liked 'DevOgabek' posts, and added comments"))
