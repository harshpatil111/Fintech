from django.urls import path
from .views import QueryView, VoiceView

urlpatterns = [
    path("query", QueryView.as_view()),
    path("voice", VoiceView.as_view()),
]
