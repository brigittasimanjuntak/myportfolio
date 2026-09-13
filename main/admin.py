from django.contrib import admin
from main.models import Experience, CreativeSpace


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_ongoing")
    list_filter = ("category",)
    search_fields = ("title", "description")


@admin.register(CreativeSpace)
class CreativeSpaceAdmin(admin.ModelAdmin):
    list_display = ("title", "medium", "created_at")
    list_filter = ("medium",)
    search_fields = ("title", "description")