# apps/common/urls.py
from django.urls import path
from .views import NotificationsListView, NotificationMarkReadView

urlpatterns = [
    path('list', NotificationsListView.as_view()),            # GET /api/notifications/list
    path('mark-read/<int:pk>', NotificationMarkReadView.as_view()),  # POST /api/notifications/mark-read/1
]
