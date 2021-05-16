from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login, get_user_model
from .models import Friend_Request, User
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages

from .forms import CreateUserForm, EditProfile, EditUserForm


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if(user is None):
                messages.info(request, 'Username OR password is incorrect')
            else:
                login(request, user)
                return redirect('home')

    return render(request, 'ubek/login/login.html')


def index(request):
    if request.user.is_authenticated:
        return HttpResponse("<h1>Hellooo " +request.user.username+ "</h1>")
    else:
        return HttpResponse('<h1>You are not logged</h1>')


def logout_user(request):
    logout(request)
    return redirect('login')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Accout was created for ' + user)

                return redirect('login')

    context = {'form':form}
    return render(request, 'ubek/bsites/register.html', context)



@login_required(login_url='login')
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


@login_required(login_url='login')
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return  HttpResponse('friend request accepted')
    else:
        return HttpResponse('friend request not accepted')


@login_required(login_url='login')
def decline_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.delete()
        return  HttpResponse('friend request decline')
    else:
        return HttpResponse('friend request not accepted')

@login_required(login_url='login')
def cancel_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.from_user == request.user:
        friend_request.delete()
        return  HttpResponse('friend request canceled')
    else:
        return HttpResponse('friend request not canceled')



@login_required(login_url='login')
def tests(request):
    if request.user.is_authenticated:
        User = get_user_model()
        all_users = User.objects.all()
        current_user = request.user
        friends_list = request.user.friends.all()[:10]
        friends_number = current_user.friends.all().count()
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
            'friends_number': friends_number,
        }
        return render(request, 'ubek/bsites/test.html', content)
    else:
        return HttpResponse('<h1>You are not logged</h1>')



@login_required(login_url='login')
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



@login_required(login_url='login')
def editprofile(request):
    current_user = request.user
    my_friend_requests = Friend_Request.objects.filter(to_user=request.user).count()
    all_friend_requests = Friend_Request.objects.filter(to_user=request.user).first()
    form_edit = EditProfile(instance=current_user.profile)
    form = EditUserForm(instance=current_user)

    if request.method == 'POST':
        form_edit = EditProfile(request.POST, request.FILES, instance=current_user.profile)
        if form_edit.is_valid():
            form_edit.save()
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()

    content = {
            'current_user': current_user,
            'form_edit': form_edit,
            'form': form,
            'my_friend_requests': my_friend_requests,
            'all_friend_requests': all_friend_requests,
        }
    return render(request, 'ubek/bsites/editprofile.html', content)




@login_required(login_url='login')
def user_list(request):
    if request.user.is_authenticated:
        User = get_user_model()
        current_user = request.user
        all_users = User.objects.exclude(is_superuser=True).exclude(id=current_user.id).exclude(user__friends=current_user).exclude(friends=current_user).exclude(from_user__in=Friend_Request.objects.filter(to_user=current_user)).exclude(to_user__in=Friend_Request.objects.filter(from_user=current_user))
        friends_list = current_user.friends.all()[:6]
        friends_number = current_user.friends.all().count()
        fullname = current_user.first_name + " " + current_user.last_name
        about = current_user.profile.about
        avatar = current_user.profile.profile_photo
        my_friend_requests = Friend_Request.objects.filter(to_user=request.user).count()
        all_friend_requests = Friend_Request.objects.filter(to_user=request.user).first()
        my_sent_friend_requests = Friend_Request.objects.filter(from_user=request.user)
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
            'my_sent_friend_requests': my_sent_friend_requests,
            'friends_number': friends_number,
        }

        return render(request, 'ubek/friends/friends_add_list.html', content)
    else:
        return HttpResponse('<h1>You are not logged</h1>')

@login_required
def request_list(request):
    all_friend_requests = Friend_Request.objects.filter(to_user=request.user)
    return render(request, 'ubek/friends/accept_friend.html', {'all_friend_requests': all_friend_requests})


@login_required(login_url='login')
def friends_list(request):
    if request.user.is_authenticated:
        User = get_user_model()
        current_user = request.user
        all_users = User.objects.exclude(is_superuser=True).exclude(user=current_user).exclude(user__friends=current_user).exclude(friends=current_user).exclude(from_user__in=Friend_Request.objects.filter(to_user=current_user)).exclude(to_user__in=Friend_Request.objects.filter(from_user=current_user))
        friends_list = current_user.friends.all()[:6]
        friends_list_all = current_user.friends.all()
        friends_number = current_user.friends.all().count()
        fullname = current_user.first_name + " " + current_user.last_name
        about = current_user.profile.about
        avatar = current_user.profile.profile_photo
        my_friend_requests = Friend_Request.objects.filter(to_user=request.user).count()
        all_friend_requests = Friend_Request.objects.filter(to_user=request.user).first()
        my_sent_friend_requests = Friend_Request.objects.filter(from_user=request.user)
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
            'my_sent_friend_requests': my_sent_friend_requests,
            'friends_number': friends_number,
            'friends_list_all': friends_list_all,
        }
        return render(request, 'ubek/friends/friends_list.html', content)
    else:
        return HttpResponse('<h1>You are not logged</h1>')

@login_required(login_url='login')
def delete_friend(request, requestID):
    user = request.user
    myfriend = User.objects.get(id=requestID)
    user.friends.remove(requestID)
    myfriend.friends.remove(request.user)
    return  HttpResponse('friend deleted')