from django.urls import path
from .views import (
    SongListCreateView,
    SongDetailView,
    PlaylistListCreateView,
    PlaylistDetailView,
    register_user,
    login_user,
    logout_user,
    check_auth_status,
    LikeSongView,
    AddSongToPlaylistView,
    RemoveSongFromPlaylistView,
    RecentlyPlayedView
)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('status/', check_auth_status, name='auth-status'),
    path('logout/', logout_user, name='logout'),
    path('songs/', SongListCreateView.as_view(), name='song-list'),
    path('songs/<int:pk>/', SongDetailView.as_view(), name='song-detail'),
    path('playlists/', PlaylistListCreateView.as_view(), name='playlist-list'),
    path('playlists/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('like-song/<int:song_id>/', LikeSongView.as_view(), name='like-song'),
    path('add-song-to-playlist/<int:playlist_id>/', AddSongToPlaylistView.as_view(), name='add-song-to-playlist'),
    path('remove-song-from-playlist/<int:playlist_id>/', RemoveSongFromPlaylistView.as_view(), name='remove-song-from-playlist'),
    path('recently-played/', RecentlyPlayedView.as_view(), name='recently-played'),
]
