from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Profile
from django.contrib.auth.decorators import login_required
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from decouple import config
from interactions.models import Post
import string

EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email_input = request.POST.get("email_input")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            if User.objects.filter(email=email_input).exists():
                messages.error(request, "Email Taken")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username Taken")
                return redirect("signup")
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email_input,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                new_profile = Profile.objects.create(
                    user=user, last_name=last_name, first_name=first_name
                )
                new_profile.save()
                return redirect("signin")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("signup")
    else:
        return render(request, "registrations/signup.html")


@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            user_email = user.email
            code_and_token = send_verification_code_and_token(
                user_email,
                """Sign In Verification""",
                """To complete your sign-in, enter the verification
            code below:""",
                """If you didn't request this code, please ignore this
            message.""",
            )
            request.session["token"] = code_and_token.get("token")
            request.session["verification_code"] = code_and_token.get("code")
            request.session["user_email"] = user_email

            request.session["change_password"] = False

            return redirect("verification")
        else:
            messages.error(request, "Invalid Credentials")
            return redirect("signin")
    else:
        return render(request, "registrations/signin.html")


def generate_token(length=32):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def send_verification_code_and_token(email, title, instruction, note):
    code = "".join(str(random.randint(0, 9)) for _ in range(6))
    sender_email = config("EMAIL")
    password = config("PASSWORD")
    token = generate_token()
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = "Verification Code"

    with open("template/email/email_body.html", "r") as file:
        body_content = file.read()

    body_content_with_code = (
        body_content.replace("{verification_code}", code)
        .replace("{token}", token)
        .replace("{title}", title)
        .replace("{instruction}", instruction)
        .replace("{note}", note)
    )

    message.attach(MIMEText(body_content_with_code, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()

        return {"code": code, "token": token}

    except Exception as e:
        print(f"Error sending verification code: {e}")
        return None


def token(request, token):
    expected_token = request.session.get("token")
    user_email = request.session.get("user_email")

    if token == expected_token:
        user = User.objects.get(email=user_email)
        auth.login(request, user)
        request.session["token"] = None
        messages.success(request, "You are logged in")
        if "change_password" in request.session:
            change_password = request.session["change_password"]
            if change_password:
                request.session["change_password"] = None
                return redirect("change_password")
        return redirect("home")
    else:
        messages.error(request, "Token is not true")
        return redirect("signin")


def mask_email(email):
    username, domain = email.split("@", 1)
    masked_username = username[:3] + "*" * max(0, len(username) - 3)
    masked_domain = "*" * max(0, len(domain) - 3)
    masked_email = f"{masked_username}@{masked_domain}com"

    return masked_email


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email)

        if user.exists():
            user_email = user.first().email
            code_and_token = send_verification_code_and_token(
                user_email,
                """Password Change Request""",
                """You have requested to change your password. Please
            use the verification code below:""",
                """Please keep this code confidential and do not share it
            with anyone. If you didn't request this change, you can safely ignore
            this email.""",
            )
            request.session["token"] = code_and_token.get("token")
            request.session["verification_code"] = code_and_token.get("code")
            request.session["user_email"] = user_email
            request.session["change_password"] = True
            return redirect("verification")
        else:
            messages.error(request, "Email not available")
            return redirect("reset_password")
    else:
        return render(request, "registrations/reset_password.html")


@login_required(login_url="reset_password")
def change_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        user = request.user

        if password == confirm_password:
            user.set_password(password)
            user.save()
            auth.login(request, user)
            messages.success(request, "Password changed successfully")
            return redirect("home")
        else:
            messages.error(request, "Invalid Credentials")
            return redirect("change_password")
    else:
        return render(request, "registrations/change_password.html")


def verification(request):
    if request.method == "POST":
        user_email = request.session.get("user_email")

        if user_email:
            entered_code = request.POST.get("code-input")
            expected_code = request.session.get("verification_code")

            if entered_code == expected_code:
                user = User.objects.get(email=user_email)
                auth.login(request, user)

                # Check if the key exists in the session
                if "change_password" in request.session:
                    change_password = request.session["change_password"]
                    request.session["verification_code"] = None
                    if change_password:
                        request.session["change_password"] = None
                        return redirect("change_password")
                return redirect("home")
            else:
                messages.error(request, "Invalid code. Please try again.")
                masked_email = mask_email(user_email)
                return render(
                    request,
                    "registrations/verification.html",
                    {"masked_email": masked_email},
                )
        else:
            messages.error(request, "User email not found.")
            return redirect("signin")
    else:
        user_email = request.session.get("user_email")
        if user_email:
            masked_email = mask_email(user_email)
            return render(
                request,
                "registrations/verification.html",
                {"masked_email": masked_email},
            )
        else:
            messages.error(request, "User email not found.")
            return redirect("signin")


def profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    posts = Post.objects.filter(author=profile.user)
    like_count = sum(post.liked_by.count() for post in posts)
    like_count = format_count(like_count)
    return render(
        request,
        "profile.html",
        {
            "profile": profile,
            "posts": posts,
            "like_count": like_count,
        },
    )


def format_count(count):
    if count > 999:
        return f"{count // 1000}.{count // 100 % 10}k"
    return str(count)


@login_required(login_url="signin")
def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(author=request.user)
    like_count = sum(post.liked_by.count() for post in posts)

    return render(
        request,
        "my_profile.html",
        {"profile": profile, "posts": posts, "like_count": like_count},
    )


@login_required(login_url="signin")
def settings(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        bio = request.POST.get("bio")
        profile_img = request.FILES.get("profile_img")

        profile.first_name = first_name
        profile.last_name = last_name
        profile.bio = bio
        if profile_img:
            profile.profile_img = profile_img
        profile.save()

        messages.success(request, "Settings successfully changed")
        return redirect("my_profile")

    return render(request, "settings.html", {"profile": profile})


@login_required(login_url="signin")
def delete_account(request):
    profile = request.user.profile
    user = request.user
    profile.delete()
    user.delete()
    messages.success(request, "Your profile was successfully deleted")
    return redirect("signin")
