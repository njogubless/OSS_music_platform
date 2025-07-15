from django.db import models

from uuid import uuid4
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Contributor(models.Model):
    """
    Optional: extra profile fields for users who upload music.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=120, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.display_name or self.user.username


class License(models.Model):
    """
    A lightweight SPDX‑like license registry.
    """
    name = models.CharField(max_length=120)
    spdx_id = models.CharField(max_length=40, unique=True)
    url = models.URLField()
    text = models.TextField(blank=True)

    def __str__(self):
        return self.spdx_id


class Track(models.Model):
    """
    The canonical music asset. If you later replace a file
    (remaster, loudness fix, etc.), create a TrackVersion.
    """
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    uploader = models.ForeignKey(Contributor, on_delete=models.PROTECT, related_name="tracks")
    license = models.ForeignKey(License, on_delete=models.PROTECT)
    audio_file = models.FileField(upload_to="tracks/%Y/%m/")
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    duration_seconds = models.PositiveIntegerField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class TrackVersion(models.Model):
    """
    Immutable revisions. ‘1.0’, ‘remix’, ‘live’, etc.
    """
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="versions")
    version_label = models.CharField(max_length=40, default="1.0")
    audio_file = models.FileField(upload_to="track_versions/%Y/%m/")
    release_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("track", "version_label"),)
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.track} – {self.version_label}"


class EmbedKey(models.Model):
    """
    A per‑track token you hand to third‑party sites so they can stream
    the track via the /embed/<key>/ endpoint without full auth.

    You may attach expirations or limits if you wish.
    """
    key = models.UUIDField(default=uuid4, editable=False, unique=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="embed_keys")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)  # optional

    def __str__(self):
        return f"{self.track} [{self.key}]"
