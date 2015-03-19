import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from chat_room.forms import ChatForm, LoginForm
from chat_room.models import Message

def chat_room(request):
    name = ''
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if 'change' in request.POST:
            try:
                del request.session['name']
            except KeyError:
                pass
        else:
            if 'name' in request.session:
                name = request.session['name']
            if form.is_valid():
                name = form.cleaned_data['name']
                request.session['name'] = name
                text = form.cleaned_data['text']
                message = Message(name=name, text=text)
                message.save()
    else:
        if 'name' in request.session:
            name = request.session['name']
            form = ChatForm(initial={'name': name})
        else:
            form = ChatForm()
    messages = Message.objects.all().order_by('created_at')
    return render(request, 'chat.html', {'form': form, 'messages':messages, 'name': name})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            request.session['name'] = name
    else:
        form = LoginForm()
    if 'name' in request.session:
        url = reverse('chat')
        return HttpResponseRedirect(url)
    return render(request, 'login.html', {'form': form})
