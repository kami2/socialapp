from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Friend_Request, Profile, PostWall, CommentPost

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Friend_Request)
admin.site.register(PostWall)
admin.site.register(CommentPost)
