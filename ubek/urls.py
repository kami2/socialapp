from django.urls import path
from . import views


urlpatterns = [
    path('', views.tests, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('check', views.index),
    path('send_friend_request/<int:userID>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:requestID>/', views.accept_friend_request, name='accept friend request'),
    path('decline_friend_request/<int:requestID>/', views.decline_friend_request, name='decline_friend_request'),
    path('cancel_friend_request/<int:requestID>/', views.cancel_friend_request, name='cancel friend request'),
    path('delete_friend/<int:requestID>/', views.delete_friend, name='delete friend'),
    path('add-friend', views.user_list, name='add_friend'),
    path('re-list', views.request_list),
    path('editprofile', views.editprofile),
    path('friends_list', views.friends_list, name='friends list'),
    path('new', views.profile),
]
