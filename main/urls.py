from django.urls import path
from main.views import delete_creative_space, get_creativespaces_json, show_main, show_experience, show_creative_space, create_creative_space

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("creative-space/", show_creative_space, name="show_creative_space"),
    path("creative-space/add/", create_creative_space, name="create_creative_space"),
    path("api/creativespaces/", get_creativespaces_json, name="get_creative_spaces_json"),
    path("creative-spaces/<uuid:creative_space_id>/delete/", delete_creative_space, name="delete_creative_space"),
]