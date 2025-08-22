from django.urls import path
from .views import RegisterView, LoginView, SocialLoginView, ResetPasswordView

urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("social-login", SocialLoginView.as_view()),
    path("reset-password", ResetPasswordView.as_view()),
]
