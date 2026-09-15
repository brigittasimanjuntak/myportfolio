from django.urls import path
from main.views import show_main, show_experience, show_creative_space, create_creative_space

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("creative-space/", show_creative_space, name="show_creative_space"),
    path("creative-space/add/", create_creative_space, name="create_creative_space"),
]