from rest_framework import serializers
from .models import Track, TrackVersion, License, EmbedKey


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ("id", "name", "spdx_id", "url")


class TrackVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackVersion
        fields = ("id", "version_label", "audio_file", "created_at", "release_notes")


class TrackSerializer(serializers.ModelSerializer):
    versions = TrackVersionSerializer(many=True, read_only=True)
    license = LicenseSerializer(read_only=True)

    class Meta:
        model = Track
        fields = (
            "id",
            "title",
            "description",
            "duration_seconds",
            "license",
            "cover_image",
            "audio_file",
            "versions",
            "created_at",
        )


class EmbedKeySerializer(serializers.ModelSerializer):
    embed_url = serializers.SerializerMethodField()

    class Meta:
        model = EmbedKey
        fields = ("key", "track", "created_at", "expires_at", "embed_url")

    def get_embed_url(self, obj):
        request = self.context["request"]
        return request.build_absolute_uri(f"/embed/{obj.key}/")
