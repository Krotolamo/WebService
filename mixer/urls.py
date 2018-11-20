from django.urls import include, path
from . import views

app_name = 'mixer'
urlpatterns = [
    path('play_song/', views.PlaySongView.as_view(), name = 'play_song'),
    path('stop_song/', views.StopSongView.as_view(), name = 'stop_song'),
    path('update_song_button/', views.UpdateSongView.as_view(), name = 'update_song_button'),
    path('login_facebook/', views.LoginFacebookView.as_view(), name = 'login_facebook'),
    path('logout/', views.Logout.as_view(), name = 'logout'),
]
