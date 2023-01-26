from django.urls import path
from linktrack.views import TrackView, TrackWebhook

urlpatterns = [
    path('track/', TrackView.as_view()),
    path('webhook/', TrackWebhook.as_view())
]
