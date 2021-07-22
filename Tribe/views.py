from Playlist.models import playlist
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import CreateTribeForm, CreateMessageForm
from django.urls import reverse
from .models import members, message, tribe
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def home_view(request, *args, **kwargs):
    
    all_tribes=tribe.objects.all()
    if request.user.is_authenticated:
        chief_tribes=[]
        for i in all_tribes:
            if i.chieftain == request.user:
                chief_tribes.append(i)
                
        not_chief_tribes=list(set(all_tribes) - set(chief_tribes))

        member_tribes_qset=members.objects.filter(user=request.user)

        member_tribes=[]
        for i in member_tribes_qset:
            member_tribes.append(i.tribe)

        not_member=list(set(not_chief_tribes) - set(member_tribes))
        
        return render (request, 'home.html', {
            'chief_tribes':chief_tribes,
            'member_tribes':member_tribes,
            'other_tribes':not_member,
        })
    else:
        return render (request, 'home.html', {
            'other_tribes':all_tribes
        })

def add_tribe_view(request):
    
    if request.method== 'POST':
        form=CreateTribeForm(request.POST, request.FILES)

        if form.is_valid():
            NewTribe=form.save(commit=False)
            NewTribe.chieftain = request.user
            NewTribe=form.save()
            return HttpResponseRedirect(reverse('tribe_details', args=[NewTribe.id,]))
        else:
            messages.error(request, ('Form not filled properly.'))
    else:
        form=CreateTribeForm()
        context= {'form':form}
        return render(request, "Tribe/create_tribe.html",context)


def tribe_detail_view(request, id):
    Tribe=get_object_or_404(tribe, pk=id)
    users_qset=members.objects.filter(tribe=Tribe)
    playlists = playlist.objects.filter(tribe=Tribe)
    users=[]
    users.append(Tribe.chieftain)
    for i in users_qset:
        users.append(i.user)
    
    messages_sent=message.objects.filter(tribe=Tribe)
    message_form=CreateMessageForm()

    context ={
        'Users':users,
        'Tribe':Tribe,
        'playlists':playlists,
        'messages':messages_sent,
        'message_form':message_form,
    }
    return render (request, 'Tribe/tribe_details.html', context)


def join_tribe_view(request, id):
    if request.method =="POST":
        Tribe=get_object_or_404(tribe, pk=id)

        join=members(user=request.user, tribe=Tribe)
        join.save()
        messages.success(request, ("You have successfully joined Tribe."))
        return HttpResponseRedirect(reverse('tribe_details', args=[id,]))
    else:
        messages.success(request, ("Something went wrong."))
        return HttpResponseRedirect(reverse('tribe_details', args=[id,]))


@login_required(login_url="/login")
def kick_member_view(request, tribe_id,id): 
    context ={}
    name=get_object_or_404(User, pk=id)
    Tribe=get_object_or_404(tribe, pk=tribe_id)
    obj = get_object_or_404(members, tribe = Tribe, user = name) 
    if request.user == Tribe.chieftain or request.user.is_staff:

        if request.method =="POST": 
            
            obj.delete()
            return HttpResponseRedirect(reverse('tribe_details', args=[tribe_id,]))
  
    else:
        messages.error(request, ("You are not chieftain of this tribe, you can't kick members out."))
        return HttpResponseRedirect(reverse('tribe_details', args=[tribe_id,]))


def leave_tribe_view(request, id): 
    Tribe=get_object_or_404(tribe, pk=id)
    obj = get_object_or_404(members, tribe = Tribe, user = request.user) 
  
    if request.method =="POST": 
        
        obj.delete()
        messages.success(request, ("You successfully left the Tribe."))
        return HttpResponseRedirect(reverse('tribe_details', args=[Tribe.id,]))
    else:
        messages.error(request, ("Leaving tribe is possible only by clicking leave tribe button."))
        return render(request, "home.html", {})


@login_required(login_url="/login")
def send_message_view(request, id):
    Tribe=get_object_or_404(tribe, pk=id)
    users_qset=members.objects.filter(tribe=Tribe)
    users=[]
    for i in users_qset:
        users.append(i.user)

    users.append(Tribe.chieftain)

    if request.user in users:
        if request.method== 'POST':
            message_form=CreateMessageForm(request.POST)
        
            if message_form.is_valid():
                NewMessage=message_form.save(commit=False)
                NewMessage.tribe = Tribe
                NewMessage.user=request.user
                NewMessage=message_form.save()
            else:
                messages.success(request, ("You can't send empty messages. "))
        return HttpResponseRedirect(reverse('tribe_details', args=[id,]))
    else:
        messages.info(request, ('Only tribe members can send messages!'))
        return HttpResponseRedirect(reverse('tribe_details', args=[id,]))


@login_required(login_url="/login")
def delete_message_view(request, id, tribe_id):
    if request.method== 'POST':
        Tribe=get_object_or_404(tribe, pk=tribe_id)
        Mess=get_object_or_404(message, pk=id)
        
        if request.user == Tribe.chieftain or request.user == Mess.user or request.user.is_staff:
            Mess.delete()
            return HttpResponseRedirect(reverse('tribe_details', args=[tribe_id,]))
    else:
        return HttpResponseRedirect(reverse('tribe_details', args=[tribe_id,]))