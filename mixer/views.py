from django.shortcuts import get_object_or_404
from .models import ButtonSong
from django.contrib.auth.models import User
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
from allauth.socialaccount.models import SocialAccount, SocialToken
import os
import RPi.GPIO as GPIO
import time


# View para reproducir una canción
# Por POST: {'button': (posicion botón),'user': (id del usuario)}
class PlaySongView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *arg, **kwargs):
        data = request.POST
        user = User.objects.get(id = data['user'])
        row = ButtonSong.objects.filter(user=user, button=data['button']).count()
        if row > 0:
            object = ButtonSong.objects.get(user=user, button=data['button'])
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(12, GPIO.OUT)
            GPIO.output(12, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(12, GPIO.LOW)
            GPIO.cleanup()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# View para detener una canción
# Por POST: {'button': (posicion botón),'user': (id del usuario)}
class StopSongView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *arg, **kwargs):
        data = request.POST
        user = User.objects.get(id = data['user'])
        row = ButtonSong.objects.filter(user=user, button=data['button']).count()
        if row > 0:
            object = ButtonSong.objects.get(user=user, button=data['button'])
            print("Deteniendo cancion: "+str(object.song))
            return Response(status=status.HTTP_200_OK)
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
        row = ButtonSong.objects.filter(user=user, button=data['button']).count()
        if row > 0:
            row = ButtonSong.objects.get(user=user, button=data['button'])
            row.song = data['song']
            row.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# View para obtener usuario o crear usuario a partir del login de facebook
# Por POST: {'id': (id usuario que devuelve la API de Facebook)}
class LoginFacebookView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *arg, **kwargs):
        data = request.POST
        id = data['id']
        account = SocialAccount.objects.filter(uid=id).count()
        if row > 0:
            account = SocialAccount.objects.get(uid=id)
            user = account.user
            return Response(user,status=status.HTTP_200_OK)
        else:
            user = User.objects.create(username=data['mail'],first_name=data['name'],last_name=data['last_name'],email=data['email'],password="")
            user.save()
            account = SocialAccount.objects.create(uid=id, user=user, provider="Facebook")
            account.save()
            token = SocialToken.objects.create(app=1,account=account,token=data['token'])
            token.save()
            return Response(user,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
