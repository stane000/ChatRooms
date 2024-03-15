from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Message, Room, Topic, User
from .forms import MyUserCreationForm, RoomForm, Userform
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def loginPage(request):

    page  = "login"

    # if request.user.is_authenticated:
    #     return redirect("home")

    if request.method =="POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user dos not exist")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "User name or password dos not exist")
    context = {"page": page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

# def registerUser(request):
#     form = UserCreationForm()
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()
#             login(request, user)
#             redirect("home")
#         else:
#             messages.error(request, "An error occured during registration")
#     return render(request, "base/login_register.html", {"form": form})

def registerUser(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # username = user.username.lower()
            # user_exist = User.objects.find(username=username)
            # if user_exist:
            #     messages.error(request, 'User Exist')
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, f'An error occurred during registration: {str(form.errors)}')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') or ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))
    rooms_count=rooms.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__name__icontains=q))
    context = {'rooms': rooms, "topics": topics, "rooms_count": rooms_count, 'room_messages': room_messages}
    return render(request, "base/home.html", context)
    
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == "POST":
        Message.objects.create(user=request.user, room=room, body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect("room", pk=room.id)

    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, "base/room.html", context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, "base/profile.html", context)

@login_required(login_url="login")
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')

    context = {"form": form, 'topics': topics, 'room': None}
    return render(request, "base/create-room.html", context)

@login_required(login_url="login")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You are not allow here")

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect("home")
    context = {"form": form, 'topics': topics, 'room': room, }
    return render(request, "base/create-room.html", context)

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allow here")

    if request.method == "POST":
        room_topic = room.topic
        room.delete()
        topics = Room.objects.filter(topic=room_topic)
        if not topics:
            room_topic.delete()
        return redirect('home')

    return render(request, "base/delete.html", {"obj": room})

def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowd here")

    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": message})

@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = Userform(instance=user)
    
    if request.method == "POST":
        form = Userform(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", pk=user.id)
    return render(request, "base/update-user.html", {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "base/topics.html", {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, "base/activity.html", {'room_messages': room_messages})
