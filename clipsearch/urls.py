from django.urls import path
from .views import clip_search_view

urlpatterns = [
    path('search/', clip_search_view),
]
