from django.urls import path
from main.views import (
    create_creative_space,
    delete_creative_space,
    get_creativespaces_json,
    login_user,
    logout_user,
    register,
    show_creative_space,
    show_experience,
    show_main,
    update_creative_space,
    toggle_star,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("creative-space/", show_creative_space, name="show_creative_space"),
    path("creative-space/add/", create_creative_space, name="create_creative_space"),
    path("api/creativespaces/", get_creativespaces_json, name="get_creative_spaces_json"),
    path("creative-spaces/<uuid:creative_space_id>/delete/", delete_creative_space, name="delete_creative_space"),
    path("creative-space/<uuid:creative_space_id>/edit/", update_creative_space, name="update_creative_space"),
    path("login/", login_user, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout_user, name="logout"),
    path("creative-space/<uuid:creative_space_id>/star/", toggle_star, name="toggle_star"),
]