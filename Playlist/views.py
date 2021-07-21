from django.shortcuts import render, get_object_or_404,redirect
from .models import playlist
from .forms import CreatePlaylistForm
from Tribe.models import tribe
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="/login")
def create_playlist_view(request, id):
    Tribe=get_object_or_404(tribe, pk=id)
    if request.user == Tribe.chieftain or request.user.is_staff:
        if request.method== 'POST':
            form=CreatePlaylistForm(request.POST)
            
            if form.is_valid():
                NewPlaylist=form.save(commit=False)
                NewPlaylist.tribe = Tribe
                NewPlaylist=form.save()
                messages.success(request, ('Playlist successfully created.'))
                return HttpResponseRedirect(reverse('tribe_details', args=[Tribe.id,]))

        else:
            form=CreatePlaylistForm()
            context= {'form':form}
            return render(request, "Playlist/create_playlist.html",context)
    else:
        messages.error(request, ('Only chieftain can create new Playlist.'))
        return HttpResponseRedirect(reverse('tribe_details', args=[id,]))

@login_required(login_url="/login")
def playlist_edit_view (request, id):
    my_tribe=get_object_or_404(playlist, pk=id).tribe
    if request.user == my_tribe.chieftain:
        thisplaylist=get_object_or_404(playlist, pk=id)
        if request.method == 'POST':
            
            playlist_form = CreatePlaylistForm(request.POST, instance=thisplaylist)
            if  playlist_form.is_valid():

                playlist_form.save()
                
                messages.success(request, ('Your playlist was successfully updated!'))
                return HttpResponseRedirect(reverse('tribe_details', args=[my_tribe.id,]))
            else:
                messages.error(request, ('Please correct the error below.'))
        else:
            playlist_form = CreatePlaylistForm(instance=thisplaylist)
            
        return render(request, 'Playlist/create_playlist.html', {
            'form': playlist_form
        })
    else:
        messages.info(request, ('Only chieftain can edit playlist info! You can ask him in chat :)'))
        return HttpResponseRedirect(reverse('playlist_detail', args=[id,]))


@login_required(login_url="/login")
def playlist_delete_view(request, id):
    my_tribe=get_object_or_404(playlist, pk=id).tribe
    if request.user == my_tribe.chieftain: 
        context ={} 
        obj = get_object_or_404(playlist, pk = id) 
    
        if request.method =="POST": 
            
            obj.delete()
            return HttpResponseRedirect(reverse('tribe_details', args=[my_tribe.id,]))
    
    else:
        messages.info(request, ('Only chieftain can delete playlists! You can ask him in chat :)'))
        return HttpResponseRedirect(reverse('playlist_detail', args=[id,]))