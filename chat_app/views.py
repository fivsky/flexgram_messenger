from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Room, Message

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('room_list')
    else:
        form = UserCreationForm()
    return render(request, 'chat_app/register.html', {'form': form})

@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'chat_app/room_list.html', {'rooms': rooms})

@login_required
def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    messages = room.messages.select_related('user').all()[:50]
    return render(request, 'chat_app/room_detail.html', {
        'room': room,
        'messages': messages,
    })
