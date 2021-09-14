from django.shortcuts import render, get_object_or_404,redirect
from .models import comment, playlist, song, like
from .forms import CreatePlaylistForm, AddSongForm, CreateCommentForm
from Tribe.models import members, tribe
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
        obj = get_object_or_404(playlist, pk = id) 
    
        if request.method =="POST": 
            
            obj.delete()
            return HttpResponseRedirect(reverse('tribe_details', args=[my_tribe.id,]))
    
    else:
        messages.info(request, ('Only chieftain can delete playlists! You can ask him in chat :)'))
        return HttpResponseRedirect(reverse('playlist_detail', args=[id,]))


def playlist_detail_view(request, id):
    
    Playlist = get_object_or_404(playlist, pk=id)
    Songs = song.objects.filter (playlist=Playlist)
    users_qset=members.objects.filter(tribe=Playlist.tribe)
    users=[]
    users.append(Playlist.tribe.chieftain)
    for i in users_qset:
        users.append(i.user)
    if request.user.is_authenticated:
        likes_qset=like.objects.filter(user=request.user)
        liked_songs=[]

        for i in likes_qset:
            liked_songs.append(i.song)

    all_comments=comment.objects.all()    
    comments=[]
    for x in all_comments:
        for y in Songs:
            if x.song==y:
                comments.append(x)

    comment_form=CreateCommentForm()
    if request.user.is_authenticated:
        context ={
            'playlist': Playlist,
            'songs':Songs,
            'users':users,
            'likes':liked_songs,
            'comments': comments,
            'comment_form': comment_form,
        }
        return render (request, 'Playlist/playlist_detail.html', context)
    else:
        context ={
            'playlist': Playlist,
            'songs':Songs,
            'users':users,
            'comments': comments,
        }
        return render (request, 'Playlist/playlist_detail.html', context)

@login_required(login_url="/login")
def add_song_view(request, id):
    this_tribe=get_object_or_404(playlist, pk=id).tribe
    users_qset=members.objects.filter(tribe=this_tribe)
    users=[]
    users.append(this_tribe.chieftain)
    for i in users_qset:
        users.append(i.user)

    if request.user in users:
        if request.method== 'POST':
            form=AddSongForm(request.POST)
            
            if form.is_valid():
                new_entry=form.save(commit=False)
                new_entry.user_added=request.user
                new_entry.playlist = get_object_or_404(playlist, pk=id)
                new_entry=form.save()
                return HttpResponseRedirect(reverse('playlist_detail', args=[id,]))
            else:
                messages.info(request, ('Form not filled properly'))
                form=AddSongForm()
                context= {'form':form}
                return render(request, "add_song.html",context)
        else:
            form=AddSongForm()
            context= {'form':form}
            return render(request, "add_song.html",context)
    else: 
        messages.info(request, ('You are not a member in this tribe, you cannot add songs! Join tribe to add songs'))
        return HttpResponseRedirect(reverse('playlist_detail', args=[id,]))


@login_required(login_url="/login")
def like_unlike_view(request, id, play_id):
    if request.method =="POST":
        Tribe=get_object_or_404(playlist, pk=play_id).tribe
        users_qset=members.objects.filter(tribe=Tribe)
        users=[]
        users.append(Tribe.chieftain)
        for i in users_qset:
            users.append(i.user)

        if request.user in users:

            Song = get_object_or_404(song, pk=id)
            if like.objects.filter(user=request.user, song=Song).exists():
                obj = get_object_or_404(like, user=request.user, song=Song) 
                obj.delete()
                Song.number_likes=Song.number_likes-1
                Song.save()
            else:
                new_entry=like(song=Song, user= request.user)
                new_entry.save()
                Song.number_likes=Song.number_likes+1
                Song.save()

            return HttpResponseRedirect(reverse('playlist_detail', args=[play_id,]))
        else:
            messages.info(request, ('You are not a member in this tribe!'))
            return HttpResponseRedirect(reverse('playlist_detail', args=[play_id,]))
    else:
        messages.info(request, ('You must click like button to like song!'))
        return render(request, "home.html", {})


@login_required(login_url="/login")
def send_comment_view(request, id, play_id):
    Tribe=get_object_or_404(playlist, pk=play_id).tribe
    users_qset=members.objects.filter(tribe=Tribe)
    users=[]
    users.append(Tribe.chieftain)
    for i in users_qset:
        users.append(i.user)

    if request.user in users:
        if request.method== 'POST':
            comment_form=CreateCommentForm(request.POST)
        
            if comment_form.is_valid():
                new_entry=comment_form.save(commit=False)
                new_entry.song = get_object_or_404(song, pk=id)
                new_entry.user=request.user
                new_entry.song.number_comments=new_entry.song.number_comments+1
                new_entry=comment_form.save()
                new_entry.song.save()
                return HttpResponseRedirect(reverse('playlist_detail', args=[play_id,]))
            else:
                messages.success(request, ('You can not submit empty comment!'))

    else:
        messages.info(request, ('Only members can comment on Songs!'))
        return HttpResponseRedirect(reverse('playlist_detail', args=[play_id,]))


def delete_song_view(request, id):
    Song=get_object_or_404(song, pk=id)
    return_id=Song.playlist.id
    if request.method == 'POST':
        if request.user == Song.playlist.tribe.chieftain or request.user == Song.user_added or request.user.is_staff: 
            context ={}
            Song.delete()
            messages.info(request, ('Song deleted successfuly'))
            return HttpResponseRedirect(reverse('playlist_detail', args=[return_id,]))
    
    else:
        messages.info(request, ('You can delete songs only by clicking delete button .'))
        return HttpResponseRedirect(reverse('playlist_detail', args=[return_id,]))


def delete_comment_view(request, id):
    Comment=get_object_or_404(comment, pk=id)
    return_id=Comment.song.playlist.id
    if request.method == 'POST':
        if request.user == Comment.song.playlist.tribe.chieftain or request.user == Comment.user or request.user.is_staff: 
            context ={}
            Comment.song.number_comments=Comment.song.number_comments-1
            Comment.song.save()
            Comment.delete()
            messages.info(request, ('Comment deleted successfuly'))
            return HttpResponseRedirect(reverse('playlist_detail', args=[return_id,]))
    
    else:
        messages.info(request, ('You can delete comments only by clicking delete button .'))
        return HttpResponseRedirect(reverse('playlist_detail', args=[return_id,]))