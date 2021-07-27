from django.forms import ModelForm
from Playlist.models import playlist,song, comment

class CreatePlaylistForm(ModelForm):
    class Meta:
        model = playlist
        fields=['name', 'description',]


class AddSongForm(ModelForm):
    class Meta:
        model = song
        fields=['artist', 'title', 'url', 'duration',]


class CreateCommentForm(ModelForm):
    class Meta:
        model = comment
        fields=['text',]