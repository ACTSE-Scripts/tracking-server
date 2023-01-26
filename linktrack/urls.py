from django.urls import path
from linktrack.views import TrackView

urlpatterns = [
    path('track/', TrackView.as_view()),
]
