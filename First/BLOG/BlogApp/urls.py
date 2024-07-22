from django.urls import path
from .views import RegistrationView,Loginview,LogoutView,PostListView,PostDetailView
urlpatterns = [
    path('signup/',RegistrationView.as_view(),name='signup'),
    path('login/',Loginview.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('posts/',PostListView.as_view(),name='posts'),
    path('posts/<int:pk>/',PostDetailView.as_view(),name='postDetail'),
]

