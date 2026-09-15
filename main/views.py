from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import CreativeSpace, Experience, CreativeSpaceForm


def show_main(request):
    context = {
        "name": "Brigitta",
        "npm": "2506601855",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "I'm an IS student from Universitas Indonesia. I have deep passion in visual design and user experience,/n"
            "aiming to create comfortable and appealing digital experiences. Nice to meet you!"
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Brigitta",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_creative_space(request):
    context = {
        "name": "Brigitta",
        "artwork_list": CreativeSpace.objects.all().order_by("-created_at"),
    }
    return render(request, "creative_space.html", context)

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
    return render(request, "creative_space_form.html", context)
