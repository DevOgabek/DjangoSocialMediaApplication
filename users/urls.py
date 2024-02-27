from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('signup/', views.signup, name='signup'),
    path('token/<str:token>/', views.token, name='token'),
    path('verification/', views.verification, name='verification'),
    path('change_password/', views.change_password, name='change_password'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('profile/<int:profile_id>/', views.profile_detail, name='profile_detail'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
]