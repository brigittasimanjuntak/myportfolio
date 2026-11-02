from django.urls import path
from main import api_views

app_name = "api"

urlpatterns = [
    path("creativespaces/", api_views.creativespace_list, name="creativespace-list"),
    path("creativespaces/<uuid:creative_space_id>/", api_views.creativespace_detail, name="creativespace-detail"),
    path("creativespaces/<uuid:creative_space_id>/star/", api_views.creativespace_star, name="creativespace-star"),
]