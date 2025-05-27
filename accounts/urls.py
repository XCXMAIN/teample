from django.urls import path
from .views import login_view, logout_view, RegisterView
# clip_search_view import 임시 주석
# from .views import clip_search_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('clip/search/', clip_search_view, name='clip_search'), # 임시 주석
]