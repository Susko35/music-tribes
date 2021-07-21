"""MusicTribes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from Profile.views import login_view, register_view, logout_view, edit_user_view

from Tribe.views import home_view, add_tribe_view, tribe_detail_view, join_tribe_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('registration/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('edit_user/', edit_user_view, name='edit_user'),

    path('add_tribe/', add_tribe_view, name='add_tribe'),
    path('tribe_details/<int:id>', tribe_detail_view, name='tribe_details'),
    path('join_tribe/<int:id>', join_tribe_view, name='join_tribe'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
