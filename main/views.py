from django.shortcuts import render

from main.models import Experience


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