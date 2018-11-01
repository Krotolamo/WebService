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
import os


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
            print("Reproduciendo cancion: "+str(object.song))
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
