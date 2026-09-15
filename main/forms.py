from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import CreativeSpace

class CreativeSpaceForm(ModelForm):
    class Meta:
        model = CreativeSpace
        fields = [
            "title",
            "description",
            "medium",
            "artist_url",
            "art_url",
        ]

        labels = {
            "title": "Title",
            "description": "Description",
            "medium": "Art Medium",
            "artist_url": "Artist Credit",
            "art_url": "Your artwork URL",
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
            "medium": TextInput(
                attrs={
                    "placeholder": "Please specify the medium of your art (e.g., digital-art, traditional, sketch, 3d-model, photography, other)",
                }
            ),
            "artist_url": URLInput(
                attrs={
                    "placeholder": "Credit the artist if it's not your own artwork!",
                }
            ),
            "art_url": URLInput(
                attrs={
                    "placeholder": "Place your artwork URL here!",
                }
            ),
        }