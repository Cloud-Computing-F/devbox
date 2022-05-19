from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    
    path('accounts/', include('allauth.urls')),
    # path('github/login/', views.github_login, name='github_login'),
    # path('github/callback/', views.github_callback, name='github_callback'),
    # path('github/login/finish/', views.GithubLogin.as_view(), name='github_login_todjango'),
]
