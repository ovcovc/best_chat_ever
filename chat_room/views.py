import datetime
from django.shortcuts import render

# Create your views here.
from chat_room.forms import ChatForm
from chat_room.models import Message


def chat_room(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']
            message = Message(name=name, text=text)
            message.save()
    else:
        form = ChatForm()
    messages = Message.objects.all().order_by('-created_at')
    return render(request, 'chat.html', {'form': form, 'messages':messages})