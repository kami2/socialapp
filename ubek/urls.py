from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_user),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register),
    path('check', views.index),
    path('send_friend_request/<int:userID>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:requestID>/', views.accept_friend_request, name='accept friend request'),
    path('decline_friend_request/<int:requestID>/', views.decline_friend_request, name='decline_friend_request'),
    path('add-friend', views.user_list, name='add_friend'),
    path('re-list', views.request_list),
    path('', views.tests),
    path('editprofile', views.editprofile),
    path('new', views.profile),
]
