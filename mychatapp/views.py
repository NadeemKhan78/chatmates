from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Profile, ChatMessage, FriendRequest
from .forms import ChatMessageForm
from django.http import JsonResponse
from .forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
import json


@login_required(login_url='mychat:login')
def index(request):
    user = request.user.profile
    friends = user.friends.all()
    context = {"user": user, "friends": friends}
    return render(request, 'mychatapp/index.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect("mychat:index")
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            form.save()

            username = request.POST["username"]
            password = request.POST["password1"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("mychat:index")
            
    context = {'form': form}
    return render(request, 'mychatapp/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect("mychat:index")
    
    error_msg = None
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("mychat:index")
        else:
            error_msg = "Invalid Credentials"

    context = {"msg": error_msg}
    return render(request, 'mychatapp/login.html', context)


def log_out(request):
    logout(request)
    return redirect("mychat:login")


@login_required(login_url='mychat:login')
def update_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("mychat:index")
    context = {"form": form}
    return render(request, "mychatapp/update.html", context)


@login_required(login_url='mychat:login')
def add_friend(request, *args, **kwargs):
    context = {}
    all_user = get_user_model()
    user = request.user
    profile = Profile.objects.get(user=user)
    profile_friends = profile.friends.all()

    suggestions_friends = all_user.objects.exclude(id__in = profile_friends).exclude(profile=profile)
    friend_requests = FriendRequest.objects.filter(receiver__in = suggestions_friends, sender = request.user) 
    context["s_friends"] = suggestions_friends
    context["f_requests"] = friend_requests

    if 'q' in request.GET:
        q = request.GET['q']
        data = Profile.objects.filter(name__icontains = q).exclude(id__in = profile_friends)
        data_friends = Profile.objects.filter(name__icontains = q).filter(id__in = profile_friends)
        context['data'] = data
        context['data_friends'] = data_friends

    return render(request, "mychatapp/add_friend.html", context)


def remove_friend(request, pk):
    user = get_user_model()
    n_user = user.objects.get(profile__id = pk)
    profile = Profile.objects.get(user_id = request.user.id)
    profile2 = Profile.objects.get(id = pk)
        
    if profile:
            profile.friends.remove(n_user)
            print(profile2)

    if profile2:
            profile2.friends.remove(request.user.id)
            print(request.user)

    
    return redirect("mychat:index")


def send_friend_request(request):
    data = json.loads(request.body)
    user = get_user_model()
    receiver = user.objects.get(id = data)
    friend_request = FriendRequest.objects.create(sender=request.user, receiver=receiver)

    return JsonResponse("it is giving", safe=False)


@login_required(login_url='mychat:login')
def friend_request_notification(request):
    user = request.user
    friend_requests = FriendRequest.objects.filter(receiver = user)
    friend_requests.update(seen=True)
    context = {"f_requests": friend_requests}
    return render(request, "mychatapp/friend_request.html", context)


def accept_friend_request(request):
    id = json.loads(request.body)
    user_id = id
    print(user_id)
    user = get_user_model()
    n_user = user.objects.get(id = user_id)
    profile = Profile.objects.get(user_id = request.user.id)
    profile2 = Profile.objects.get(user_id = user_id)

    msg = None

    if profile:

        if profile.friends.filter(id=user_id).exists():
            profile.friends.remove(n_user)
            FriendRequest.objects.filter(receiver = request.user, sender = user_id).delete()
            msg = "No"

        else:
            profile.friends.add(n_user)
            FriendRequest.objects.filter(receiver = request.user, sender = user_id).delete()
            msg = "Yes"

    if profile2:

        if profile2.friends.filter(id=request.user.id).exists():
            profile2.friends.remove(request.user)
            FriendRequest.objects.filter(receiver = user_id, sender = request.user).delete()

        else:
            profile2.friends.add(request.user)
            FriendRequest.objects.filter(receiver = user_id, sender = request.user).delete()

    return JsonResponse(msg, safe=False)


@login_required(login_url='mychat:login')
def chatroom(request, pk):
    friend = Profile.objects.get(id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.id)
    form = ChatMessageForm()
    chats = ChatMessage.objects.all()
    rec_chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    rec_chats.update(seen=True)

    if request.method == "POST":
        form = ChatMessageForm(request.POST)

        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect("mychat:chatroom", pk=friend.profile.id)

    context = {"friend": friend, "form": form, "user": user, "profile": profile, "chats": chats, "chat_count": rec_chats.count()}
    return render(request, 'mychatapp/chat.html', context)


def sentMessages(request, pk):
    user = request.user.profile
    friend = Profile.objects.get(id=pk)
    profile = Profile.objects.get(id=friend.id)
    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_receiver=profile, seen=False)
    print(new_chat)
    return JsonResponse(new_chat_message.body, safe=False)


def receivedMessages(request, pk):
    user = request.user.profile
    friend = Profile.objects.get(id=pk)
    profile = Profile.objects.get(id=friend.id)
    arr = []
    chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    for chat in chats:
        arr.append(chat.body)

    return JsonResponse(arr, safe=False)


def chatNotification(request):
    user = request.user.profile
    friends = user.friends.all()
    arr = []
    for friend in friends:
        chats = ChatMessage.objects.filter(msg_sender__id=friend.profile.id, msg_receiver=user, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)


def requestNotification(request):
    user = request.user
    arr_req = []

    requests = FriendRequest.objects.filter(receiver = user, seen = False)
    arr_req.append(requests.count())
    
    return JsonResponse(arr_req, safe=False)


# Responsive views

@login_required(login_url='mychat:login')
def my_profile(request):
    user = request.user.profile
    context = {"user": user}
    return render(request, "mychatapp/my_profile.html", context)

