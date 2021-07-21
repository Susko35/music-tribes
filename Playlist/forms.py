from django.forms import ModelForm
from Playlist.models import playlist

class CreatePlaylistForm(ModelForm):
    class Meta:
        model = playlist
        fields=['name', 'description',]