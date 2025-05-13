from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Song, Playlist, Favorite
from .serializers import SongSerializer, PlaylistSerializer, FavoriteSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()

    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": "Invalid token or logout failed"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_auth_status(request):
    user = request.user
    return Response({"message": "Authenticated", "username": user.username}, status=status.HTTP_200_OK)

class SongListCreateView(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class SongDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]


class PlaylistListCreateView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]


# Like/Unlike a Song
class LikeSongView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, song_id):
        user = request.user
        song = get_object_or_404(Song, id=song_id)

        # Toggle Like
        if Favorite.objects.filter(user=user, song=song).exists():
            Favorite.objects.filter(user=user, song=song).delete()
            return Response({"message": "Song unliked"}, status=status.HTTP_200_OK)
        else:
            Favorite.objects.create(user=user, song=song)
            return Response({"message": "Song liked"}, status=status.HTTP_201_CREATED)


# Add Song to Playlist
class AddSongToPlaylistView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, playlist_id):
        user = request.user
        song_id = request.data.get('song_id')
        playlist = get_object_or_404(Playlist, id=playlist_id, user=user)
        song = get_object_or_404(Song, id=song_id)

        playlist.songs.add(song)
        return Response({"message": "Song added to playlist"}, status=status.HTTP_200_OK)


# Remove Song from Playlist
class RemoveSongFromPlaylistView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, playlist_id):
        user = request.user
        song_id = request.data.get('song_id')
        playlist = get_object_or_404(Playlist, id=playlist_id, user=user)
        song = get_object_or_404(Song, id=song_id)

        playlist.songs.remove(song)
        return Response({"message": "Song removed from playlist"}, status=status.HTTP_200_OK)


# Recently Played Songs
class RecentlyPlayedView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Song.objects.order_by('-play_count')[:10]

    serializer_class = SongSerializer
