from django.forms import ModelForm, Select, TextInput, Textarea, URLInput

from main.models import CreativeSpace

class CreativeSpaceForm(ModelForm):
    class Meta:
        model = CreativeSpace
        fields = [
            "title",
            "description",
            "artist",
            "medium",
            "image",
        ]

        labels = {
            "title": "Title",
            "description": "Description",
            "artist": "Artist",
            "medium": "Art Medium",
            "image": "Artwork URL",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Share your masterpieces! (NO NSFW / Fetish / Hate/ Gore / etc, please! This is a safe space for everyone!)",
                    "rows": 3,
                }
            ),
            "medium": Select(),
            "artist": TextInput(
                attrs={
                    "placeholder": "Enter the artist's name!",
                }
            ),
            "image": URLInput(
                attrs={
                    "placeholder": "Place your artwork URL here!",
                }
            ),
        }