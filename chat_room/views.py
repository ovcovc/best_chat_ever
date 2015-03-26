import datetime
import random
import string
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from gcm import GCM
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
    google_id_2 = "APA91bFOG6hT3hNIhYP2YHtxLKCATDWKolIIKdkaj8_AHbWDnVxHmEJuPorVTByYWsyiSInYmfD9NnDzX-73LFBQpObffxWzUc-wRbxxD08f-0HjHBSQMihoVYeCC-E8EH-99SLrfbM43qBqbA_8TdFCaUNRR6Qt-Q"
    google_api_key = "AIzaSyDVO2LlKyohK8_HSv1nx1S5J6ajz_1oGUU"
    google_id = "APA91bEJ4HdNXmXLCnJTNxZzgiUCoew_agq-xdOksd0okpnFLPwmMoPUXst2WdspXA9gkd-U6TF1MaNImVHO1w2rVuHBPR_vAddP7e8YUlrW7PLLfdi9OoX99ugiJymp9prYBbuHh2dKSnwZXdMUiBx718itf8C5kg"
    gcm = GCM(google_api_key)
    key = "45189182"
    secret = "892545526be847347ac168b75f0be0cbe7902e49"
    opentok_sdk = OpenTok(key, secret)
    session = opentok_sdk.create_session(media_mode=MediaModes.routed)
    print session.session_id
    token = opentok_sdk.generate_token(session.session_id)
    print "token " + token
    data = {'token': token, 'sesja': session.session_id}
    response = gcm.json_request(registration_ids=[google_id_2,], data=data)
    return render(request, 'video_chat.html', {'API_KEY': key, 'SESSION_ID': session.session_id, "TOKEN": token})


#APIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPIAPI

def token_generator(size=24, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@api_view(['GET'])
def all_consultants(request):
    if request.method == 'GET':
        consultants = Consultant.objects.all()
        serializer = ConsultantSerializer(consultants, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_consultant(request):
    token = token_generator()
    data = {'name': request.DATA.get('name'), 'password': request.DATA.get('password'), 'google_id': request.DATA.get('google_id'), 'active_token': token}
    serializer = ConsultantSerializer(data=data)
    if serializer.is_valid():
        for c in Consultant.objects.filter(google_id = request.DATA.get('google_id')):
            c.google_id = ""
            c.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def log_in(request):
    name = request.DATA.get('name')
    password = request.DATA.get('password')
    try:
        consultant = Consultant.objects.get(name=name, password=password)
    except Consultant.DoesNotExist:
        return HttpResponse(status=404)
    token = token_generator()
    data = {'active_token': token}
    serializer = ConsultantSerializer(consultant, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def log_out(request):
    token = request.data.get('token')
    if not token:
        return HttpResponse(status=403)
    try:
        consultant = Consultant.objects.get(pk=request.data.get('id'))
    except Consultant.DoesNotExist:
        return HttpResponse(status=404)
    if token is not consultant.active_token:
        return HttpResponse(status=403)
    data = {'is_active': False, 'active_token': ""}
    serializer = ConsultantSerializer(consultant, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def set_consultant_available(request, id):
    token = request.data.get('token')
    if not token:
        return HttpResponse(status=403)
    try:
        consultant = Consultant.objects.get(pk=id)
    except Consultant.DoesNotExist:
        return HttpResponse(status=404)
    if token is not consultant.active_token:
        return HttpResponse(status=403)
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
    token = request.data.get('token')
    if not token:
        return HttpResponse(status=403)
    if token is not consultant.active_token:
        return HttpResponse(status=403)
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
    token = request.data.get('token')
    if not token:
        return HttpResponse(status=403)
    if token is not consultant.active_token:
        return HttpResponse(status=403)
    data = {'is_available': False}
    serializer = ConsultantSerializer(consultant, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

