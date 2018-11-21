from django.shortcuts import get_object_or_404
from .models import ButtonSong
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
import os
import subprocess, signal, time
import multiprocessing
#import alsaaudio

def buttons(user):
    button1 = ButtonSong.objects.create(user=user, button="1")
    button1.save()
    button2 = ButtonSong.objects.create(user=user, button="2")
    button2.save()
    button3 = ButtonSong.objects.create(user=user, button="3")
    button3.save()
    button4 = ButtonSong.objects.create(user=user, button="4")
    button4.save()
    button5 = ButtonSong.objects.create(user=user, button="5")
    button5.save()
    button6 = ButtonSong.objects.create(user=user, button="6")
    button6.save()

def stop():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    a=[]
    for i in out:
        a.append(chr(i))
        #a.split('\n')
    a="".join(a)
    a=a.split('\n')

    for line in a:
        if 'omxplayer' in line:
            line=line.split()
            pid = int(line[0])
            os.kill(pid, signal.SIGKILL)

def volume(x):
    #sudo apt-get install python-alsaaudio
    m = alsaaudio.Mixer()
    #m = alsaaudio.Mixer('PCM')
    current_volume = m.getvolume() # Get the current Volume
    m.setvolume(x)

def playsound(filedir):
    subprocess.call(['omxplayer', filedir])

def multithread(filedir):
    print(filedir)
    p = multiprocessing.Process(target=playsound, args=(filedir,))
    p.start()
    return 0

# View para reproducir una canción
# Por POST: {'button': (posicion botón),'user': (id del usuario)}
class PlaySongView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *arg, **kwargs):
        id = request.data['user']
        button = request.data['button']
        user = User.objects.get(id = id)
        row = ButtonSong.objects.filter(user=user, button=button).count()
        if row > 0:
            object = ButtonSong.objects.get(user=user, button=button)
            #llamada a modulo omxplayer
            multithread(str(object.song.path))
            serializer = SongSerializer(object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# View para detener una canción
# Por POST: {'button': (posicion botón),'user': (id del usuario)}
class StopSongView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *arg, **kwargs):
        data = request.data
        user = User.objects.get(id = data['user'])
        if user:
            stop()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# View para modificar canción de cierto botón
# Por POST: {'button': (posicion botón),'user': (id del usuario), 'song': (canción para el botón)}
#También se tiene que enviar el archivo por POST
class UpdateSongView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *arg, **kwargs):
        data = request.data
        user = User.objects.get(id = data['user'])
        row = ButtonSong.objects.get(user=user, button=data['button'])
        serializer = SongSerializer(row, data = request.data)
        if serializer.is_valid():
            if row.song :
                os.remove(row.song.path)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# View para obtener usuario o crear usuario a partir del login de facebook
# Por POST: {'id': (id usuario que devuelve la API de Facebook)}
class LoginFacebookView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *arg, **kwargs):
        data = request.data
        account = SocialAccount.objects.filter(uid=data['id']).count()
        app = SocialApp.objects.get(id=1)
        if account > 0:
            account = SocialAccount.objects.get(uid=data['id'])
            token = SocialToken.objects.create(app=app,account=account,token=data['token'])
            token.save()
            user = account.user
            serializer = UserSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            user = User.objects.create(username=data['email'],first_name=data['first_name'],last_name=data['last_name'],email=data['email'],password="")
            user.save()
            buttons(user)
            account = SocialAccount.objects.create(uid=data['id'], user=user, provider="Facebook")
            account.save()
            token = SocialToken.objects.create(app=app,account=account,token=data['token'])
            token.save()
            serializer = UserSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *arg, **kwargs):
        data = request.data
        user = User.objects.get(id=data['user'])
        account = SocialAccount.objects.get(user=user)
        token = SocialToken.objects.get(account=account)
        token.delete()
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ChangeVolume(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *arg, **kwargs):
        data = request.data
        user = User.objects.get(id = data['user'])
        if user:
            #volume(data['volume'])
            print("Volume set to "+ data['volume'] )
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
