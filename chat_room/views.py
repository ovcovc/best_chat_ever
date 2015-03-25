import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from opentok import OpenTok, MediaModes
import opentok
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from chat_room.forms import ChatForm, LoginForm
from chat_room.models import Message, Consultant
from chat_room.serializers import ConsultantSerializer


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
                form = ChatForm(initial={'name': name})
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

def video_chat(request):
    key = "45189182"
    secret = "892545526be847347ac168b75f0be0cbe7902e49"
    opentok_sdk = OpenTok(key, secret)
    session = opentok_sdk.create_session(media_mode=MediaModes.routed)
    print session.session_id
    token = opentok_sdk.generate_token(session.session_id)
    print "token " + token
    return render(request, 'video_chat.html', {'API_KEY': key, 'SESSION_ID': session.session_id, "TOKEN": token})


#APIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPI

@api_view(['GET'])
def all_consultants(request):
    if request.method == 'GET':
        consultants = Consultant.objects.all()
        serializer = ConsultantSerializer(consultants, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_consultant(request):
    data = {'name': request.DATA.get('name'), 'password': request.DATA.get('password'), 'google_id': request.DATA.get('google_id')}
    serializer = ConsultantSerializer(data=data)
    if serializer.is_valid():
        for c in Consultant.objects.filter(google_id = request.DATA.get('google_id')):
            c.google_id = ""
            c.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
def set_consultant_available(request, id):
    try:
        consultant = Consultant.objects.get(pk=id)
    except Consultant.DoesNotExist:
        return HttpResponse(status=404)
    data = {'is_available': True}
    serializer = ConsultantSerializer(consultant, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_google_id(request, id):
    try:
        consultant = Consultant.objects.get(pk=id)
    except Consultant.DoesNotExist:
        return HttpResponse(status=404)
    data = {'google_id': request.DATA.get('google_id')}
    serializer = ConsultantSerializer(consultant, data=data, partial=True)
    if serializer.is_valid():
        for c in Consultant.objects.filter(google_id = request.DATA.get('google_id')):
            if c is not consultant:
                c.google_id = ""
                c.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
def set_consultant_busy(request, id):
    try:
        consultant = Consultant.objects.get(pk=id)
    except Consultant.DoesNotExist:
        return HttpResponse(status=404)
    data = {'is_available': False}
    serializer = ConsultantSerializer(consultant, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

