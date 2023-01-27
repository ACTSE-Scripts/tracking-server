from django.urls import path
from linktrack.views import TrackView, TrackWebhook, UrlBuilder

urlpatterns = [
    path('/', UrlBuilder.as_view()),
    path('webhook/', TrackWebhook.as_view()),
    path('<alias>', TrackView.as_view()),
]
