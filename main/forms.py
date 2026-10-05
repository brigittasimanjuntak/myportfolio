from django.forms import ModelForm, Select, TextInput, Textarea, URLInput
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags 
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
                    "placeholder": "Your Artwork Title Here!",
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
            ),}
    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        cleaned = strip_tags(title).strip()
        if not cleaned:
            raise ValidationError("Title tidak boleh kosong atau cuma berisi tag HTML.")
        return cleaned

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        return strip_tags(description).strip() if description else description

    def clean_artist(self):
        artist = self.cleaned_data.get("artist", "")
        return strip_tags(artist).strip() if artist else artist