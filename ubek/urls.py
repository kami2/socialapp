from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.registerPage, name='register'),


    path('send_friend_request/<int:userID>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:requestID>/', views.accept_friend_request, name='accept friend request'),
    path('decline_friend_request/<int:requestID>/', views.decline_friend_request, name='decline_friend_request'),
    path('cancel_friend_request/<int:requestID>/', views.cancel_friend_request, name='cancel friend request'),
    path('delete_friend/<int:requestID>/', views.delete_friend, name='delete friend'),


    path('add-friend/', views.profile_friends_add, name='add_friend'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('delete_post/<int:requestID>/', views.delete_post, name='delete post'),
    path('post/<int:postID>/', views.post_detail, name='post detail'),


    path('profile/<int:profileID>/', views.profile_page, name='profile page'),
    path('profile/<int:profileID>/friends/', views.profile_friends, name='profile friends'),
    path('profile/<int:profileID>/about/', views.profile_about, name='profile about'),
]
