from rest_framework import serializers
from django.utils.html import strip_tags
from main.models import CreativeSpace


class CreativeSpaceSerializer(serializers.ModelSerializer):
    # Field tambahan buat Star (diambil dari relasi ManyToMany)
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    # Medium display (buat dapetin teks "Digital Art" bukan "digital-art")
    medium_display = serializers.CharField(source="get_medium_display", read_only=True)

    class Meta:
        model = CreativeSpace
        fields = [
            "id",
            "title",
            "description",
            "artist",
            "image",
            "medium",
            "medium_display",
            "created_at",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id", "created_at"]

    # ===== VALIDASI XSS (Sama kayak Tugas 5) =====
    def validate_title(self, value):
        # Cek apakah ada tag HTML di dalam string
        cleaned = strip_tags(value).strip()
        
        # Kalo setelah di-strip hasilnya beda, berarti user masukin tag HTML
        if cleaned != value:
            raise serializers.ValidationError("Title tidak boleh mengandung tag HTML.")
            
        # Kalo hasilnya kosong (misal cuma isi spasi)
        if not cleaned:
            raise serializers.ValidationError("Title tidak boleh kosong.")
            
        return cleaned

    def validate_description(self, value):
        return strip_tags(value) if value else value

    def validate_artist(self, value):
        return strip_tags(value) if value else value

    # ===== FUNGSI BUAT HITUNG STAR =====
    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())