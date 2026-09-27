from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied        
import datetime

from main.forms import CreativeSpaceForm
from main.models import CreativeSpace, Experience


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Brigitta",
        "npm": "2506601855",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "I'm an IS student from Universitas Indonesia. I have deep passion in visual design and user experience,\n"
            "aiming to create comfortable and appealing digital experiences. Nice to meet you!"
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Brigitta",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_creative_space(request):
    json_response = get_creativespaces_json(request)
    
    raw_objects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    artworks = [obj.object for obj in raw_objects]
    
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Brigitta",
        "artwork_list": artworks,
        "title_query": title_query,
    }
    return render(request, "creativespace.html", context)

@login_required(login_url="/login/")
def create_creative_space(request):
    form = CreativeSpaceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Congrats! New artwork has been added!")
        return redirect("main:show_creative_space")

    context = {
        "name": "Brigitta",
        "form": form,
    }
    return render(request, "creativespaceform.html", context)

@login_required(login_url="/login/")
def delete_creative_space(request, creative_space_id):
    creative_space = get_object_or_404(CreativeSpace, pk=creative_space_id)

    if request.method == "POST":
        creative_space.delete()
        messages.success(request, "Artwork deleted!")
        return redirect("main:show_creative_space")

    return redirect("main:show_creative_space")

def get_creativespaces_json(request):
    title_query = request.GET.get("title", "").strip()
    creativespaces = CreativeSpace.objects.all()

    if title_query:
        creativespaces = creativespaces.filter(title__icontains=title_query)

    creativespaces_json = serializers.serialize("json", creativespaces)
    return HttpResponse(creativespaces_json, content_type="application/json")

@login_required(login_url="/login/")
def update_creative_space(request, creative_space_id):
    artwork = get_object_or_404(CreativeSpace, pk=creative_space_id)

    if request.method == "POST":
        form = CreativeSpaceForm(request.POST, instance=artwork)
        if form.is_valid():
            form.save()
            messages.success(request, "Artwork updated!")
            return redirect("main:show_creative_space")
    else:
        form = CreativeSpaceForm(instance=artwork)

    context = {
        "name": "Brigitta",
        "form": form,
        "artwork": artwork,
    }
    return render(request, "creativespaceform.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "register.html", context)

@login_required(login_url="/login/")
def toggle_star(request, creative_space_id):
    creativespace = get_object_or_404(CreativeSpace, pk=creative_space_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in creativespace.starred_by.all():
            creativespace.starred_by.remove(request.user)
        else:
            creativespace.starred_by.add(request.user)

    return redirect("main:show_creative_space")

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response