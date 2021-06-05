from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login, get_user_model
from .models import Friend_Request, User, PostWall
from django.contrib import messages
from .forms import CreateUserForm, EditProfile, EditUserForm, PostForm, EditPostForm


def home(request):
    profileID = request.user.id
    return redirect('profile page', profileID = profileID)



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
def delete_friend(request, requestID):
    user = request.user
    myfriend = User.objects.get(id=requestID)
    user.friends.remove(requestID)
    myfriend.friends.remove(request.user)
    messages.info(request, myfriend.first_name + ' ' + myfriend.last_name + ' deleted from your friends')
    return  redirect('add_friend')



@login_required(login_url='login')
def send_friend_request(request, userID):
    User = get_user_model()
    from_user = request.user
    to_user = User.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(
        from_user=from_user, to_user=to_user)
    if created:
        messages.info(request, 'Friend request sent to ' + to_user.first_name + ' ' + to_user.last_name)
        return redirect('add_friend')
    else:
        messages.info(request, 'Friend request was already sent to ' + to_user.first_name + ' ' + to_user.last_name)
        return redirect('add_friend')



@login_required(login_url='login')
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        messages.info(request, 'Friend request accepted')
        return  redirect('add_friend')
    else:
        messages.info(request, 'Friend request not accepted')
        return redirect('add_friend')



@login_required(login_url='login')
def decline_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.delete()
        messages.info(request, 'Friend request decline')
        return redirect('add_friend')
    else:
        messages.info(request, 'Friend request not accepted')
        return redirect('add_friend')



@login_required(login_url='login')
def cancel_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.from_user == request.user:
        friend_request.delete()
        messages.info(request, 'Friend request canceled')
        return redirect('add_friend')
    else:
        messages.info(request, 'Friend request not canceled')
        return redirect('add_friend')



@login_required(login_url='login')
def profile_page(request, profileID):
    User = get_user_model()
    show_profile = User.objects.get(id=profileID)
    posts = PostWall.objects.filter(user=profileID) | PostWall.objects.filter(user__friends=profileID)
    posts_order = posts.order_by('-pub_date').distinct()
    my_friend_requests = Friend_Request.objects.filter(to_user=request.user).count()
    all_friend_requests = Friend_Request.objects.filter(to_user=request.user).first()
    friend_number = show_profile.friends.all().count()
    friends_list_all = show_profile.friends.all()[:6]
    form_edit_post = EditPostForm()
    form = PostForm()

    if request.method == 'POST' and 'Add Post' in request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user = request.user
            form_save.save()
            form = PostForm()

    if request.method == 'POST' and 'Edit Post' in request.POST:
        post_id = request.POST['Edit Post']
        form_edit_post = EditPostForm(request.POST, instance=PostWall.objects.get(id=post_id))
        if form_edit_post.is_valid():
            form_edit_post_save = form_edit_post.save(commit=False)
            form_edit_post_save.user = request.user
            form_edit_post_save.save()

    content = {
        'show_profile' : show_profile,
        'my_friend_requests': my_friend_requests,
        'all_friend_requests': all_friend_requests,
        'posts' : posts,
        'posts_order' : posts_order,
        'friend_number' : friend_number,
        'friends_list_all' : friends_list_all,
        'form' : form,
        'form_edit_post' : form_edit_post,
    }

    return render(request, 'ubek/profile/profile.html', content)



@login_required(login_url='login')
def profile_friends(request, profileID):
    User = get_user_model()
    show_profile = User.objects.get(id=profileID)
    my_friend_requests = Friend_Request.objects.filter(to_user=request.user).count()
    all_friend_requests = Friend_Request.objects.filter(to_user=request.user).first()
    friend_number = show_profile.friends.all().count()
    friends_list_all = show_profile.friends.all()[:6]
    friend_list_left = show_profile.friends.all()

    content = {
        'show_profile' : show_profile,
        'my_friend_requests': my_friend_requests,
        'all_friend_requests': all_friend_requests,
        'friend_number' : friend_number,
        'friends_list_all' : friends_list_all,
        'friend_list_left' : friend_list_left,
    }

    return render(request, 'ubek/profile/profile_friends.html', content)



@login_required(login_url='login')
def profile_about(request, profileID):
    User = get_user_model()
    show_profile = User.objects.get(id=profileID)
    my_friend_requests = Friend_Request.objects.filter(to_user=request.user).count()
    all_friend_requests = Friend_Request.objects.filter(to_user=request.user).first()
    friend_number = show_profile.friends.all().count()
    friends_list_all = show_profile.friends.all()[:6]

    content = {
        'show_profile' : show_profile,
        'my_friend_requests': my_friend_requests,
        'all_friend_requests': all_friend_requests,
        'friend_number' : friend_number,
        'friends_list_all' : friends_list_all,
    }

    return render(request, 'ubek/profile/profile_about.html', content)



@login_required(login_url='login')
def delete_post(request, requestID):
    post = PostWall.objects.get(id=requestID)
    post.delete()
    messages.info(request, 'Post deleted')
    return redirect('home')



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
def profile_friends_add(request):
    User = get_user_model()
    show_profile = request.user
    my_friend_requests = Friend_Request.objects.filter(to_user=request.user).count()
    all_friend_requests = Friend_Request.objects.filter(to_user=request.user).first()
    friend_number = show_profile.friends.all().count()
    friends_list_all = show_profile.friends.all()[:6]
    friend_list_left = show_profile.friends.all()
    test = User.objects.all()
    request_from_user = Friend_Request.objects.filter(to_user=request.user)
    my_sent_friend_requests = Friend_Request.objects.filter(from_user=request.user)
    all_users = User.objects.exclude(is_superuser=True).exclude(id=show_profile.id).exclude(
        user__friends=show_profile).exclude(friends=show_profile).exclude(
        from_user__in=Friend_Request.objects.filter(to_user=show_profile)).exclude(
        to_user__in=Friend_Request.objects.filter(from_user=show_profile))

    content = {
        'my_sent_friend_requests' : my_sent_friend_requests,
        'request_from_user' : request_from_user,
        'all_users' : all_users,
        'test' : test,
        'show_profile' : show_profile,
        'my_friend_requests': my_friend_requests,
        'all_friend_requests': all_friend_requests,
        'friend_number' : friend_number,
        'friends_list_all' : friends_list_all,
        'friend_list_left' : friend_list_left,
    }

    return render(request, 'ubek/profile/profile_friends_advanced.html', content)







