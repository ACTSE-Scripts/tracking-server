from django.urls import path
from linktrack.views import TrackView, TrackWebhook

urlpatterns = [
    path('<alias:str>', TrackView.as_view()),
    path('webhook/', TrackWebhook.as_view())
]
