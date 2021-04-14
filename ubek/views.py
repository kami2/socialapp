from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login, get_user_model
from .models import Friend_Request
from django.db.models import F



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if(username == ""): return HttpResponse("No username")
        if(password == ""): return HttpResponse("No password")
        user = authenticate(username=username, password=password)
        if(user is None): return HttpResponse("<h1>Unauthorized</h1>")
        else:
            login(request, user)
            return redirect('/')

    return render(request, 'ubek/login/login.html')


def index(request):
    if request.user.is_authenticated:
        return HttpResponse("<h1>Hellooo " +request.user.username+ "</h1>")
    else:
        return HttpResponse('<h1>You are not logged</h1>')


def logout_user(request):
    logout(request)

    return HttpResponse("<h1>logged out</h1>")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if(username == ""): return HttpResponse("No username")
        if(password == ""): return HttpResponse("No password")
        if(email == ""): return HttpResponse("No email")
        User = get_user_model()
        User.objects.create_user(username=username, password=password, email=email)
        user = authenticate(username=username, password=password)
        if (user is None): return HttpResponse("<h1>Unauthorized</h1>")
        else:
            login(request, user)
            return redirect('/')

    return render(request, 'ubek/login/register.html')

@login_required
def send_friend_request(request, userID):
    User = get_user_model()
    from_user = request.user
    to_user = User.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(
        from_user=from_user, to_user=to_user)
    if created:
        return HttpResponse('friend request sent')
    else:
        return HttpResponse('friend request was already sent')

@login_required
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return  HttpResponse('friend request accepted')
    else:
        return HttpResponse('friend request not accepted')


@login_required
def decline_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.delete()
        return  HttpResponse('friend request decline')
    else:
        return HttpResponse('friend request not accepted')

@login_required
def tests(request):
    if request.user.is_authenticated:
        User = get_user_model()
        all_users = User.objects.all()
        current_user = request.user
        friends_list = request.user.friends.all()[:10]
        fullname = current_user.first_name + " " + current_user.last_name
        about = current_user.profile.about
        avatar = current_user.profile.profile_photo
        my_friend_requests = Friend_Request.objects.filter(to_user=request.user).count()
        all_friend_requests = Friend_Request.objects.filter(to_user=request.user).first()
        content = {
            'current_user' : current_user,
            'fullname' : fullname,
            'about' : about,
            'avatar' : avatar,
            'all_users' : all_users,
            'my_friend_requests' : my_friend_requests,
            'all_friend_requests' : all_friend_requests,
            'friends_list' : friends_list,
        }
        return render(request, 'ubek/bsites/test.html', content)
    else:
        return HttpResponse('<h1>You are not logged</h1>')


def profile(request):
    if request.user.is_authenticated:
        User = get_user_model()
        all_users = User.objects.all()
        current_user = request.user
        fullname = current_user.first_name + " " + current_user.last_name
        about = current_user.profile.about
        avatar = current_user.profile.profile_photo
        content = {
            'current_user' : current_user,
            'fullname' : fullname,
            'about' : about,
            'avatar' : avatar,
            'all_users' : all_users,
        }
        return render(request, 'ubek/bsites/profile.html', content)
    else:
        return HttpResponse('<h1>You are not logged</h1>')

def editprofile(request):
    if request.user.is_authenticated:
        User = get_user_model()
        all_users = User.objects.all()
        current_user = request.user
        fullname = current_user.first_name + " " + current_user.last_name
        about = current_user.profile.about
        avatar = current_user.profile.profile_photo
        content = {
            'current_user': current_user,
            'fullname': fullname,
            'about': about,
            'avatar': avatar,
            'all_users': all_users,
        }
        return render(request, 'ubek/bsites/editprofile.html', content)
    else:
        return HttpResponse('<h1>You are not logged</h1>')




@login_required
def user_list(request):
    if request.user.is_authenticated:
        User = get_user_model()
        current_user = request.user
        all_users = User.objects.exclude(is_superuser=True).exclude(user__friends=current_user).exclude(friends=current_user).exclude(from_user__in=Friend_Request.objects.filter(to_user=current_user))
        friends_list = current_user.friends.all()[:10]
        fullname = current_user.first_name + " " + current_user.last_name
        about = current_user.profile.about
        avatar = current_user.profile.profile_photo
        my_friend_requests = Friend_Request.objects.filter(to_user=request.user).count()
        all_friend_requests = Friend_Request.objects.filter(to_user=request.user).first()
        ajc = Friend_Request.objects.filter(to_user=request.user)
        content = {
            'current_user': current_user,
            'fullname': fullname,
            'about': about,
            'avatar': avatar,
            'all_users': all_users,
            'my_friend_requests': my_friend_requests,
            'all_friend_requests': all_friend_requests,
            'friends_list': friends_list,
            'ajc': ajc,
        }
        return render(request, 'ubek/friends/friends_add_list.html', content)
    else:
        return HttpResponse('<h1>You are not logged</h1>')

@login_required
def request_list(request):
    all_friend_requests = Friend_Request.objects.filter(to_user=request.user)
    return render(request, 'ubek/friends/accept_friend.html', {'all_friend_requests': all_friend_requests})
