from django.urls import include, path
from . import views

app_name = 'mixer'
urlpatterns = [
    path('play_song/', views.PlaySongView.as_view(), name = 'play_song'),
    path('update_song_button/', views.UpdateSongView.as_view(), name = 'update_song_button'),
]
