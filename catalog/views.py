from django.shortcuts import render
from datetime import datetime
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import FileResponse

from .models import Track, TrackVersion, License, EmbedKey
from .serializers import (
    TrackSerializer,
    TrackVersionSerializer,
    LicenseSerializer,
    EmbedKeySerializer,
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Owners (uploaders) can modify, everyone can read public tracks.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.is_public or request.user.is_authenticated
        return obj.uploader.user == request.user


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.select_related("license", "uploader").all()
    serializer_class = TrackSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        contributor = self.request.user.contributor
        serializer.save(uploader=contributor)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def generate_embed_key(self, request, pk=None):
        """
        POST /tracks/<id>/generate_embed_key/
        Returns {key, embed_url}
        """
        track = self.get_object()
        key = track.embed_keys.create()
        return Response(EmbedKeySerializer(key, context={"request": request}).data)


class TrackVersionViewSet(viewsets.ModelViewSet):
    queryset = TrackVersion.objects.select_related("track").all()
    serializer_class = TrackVersionSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        parent_track = Track.objects.get(pk=self.request.data["track"])
        serializer.save(track=parent_track)


class LicenseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def embed_stream(request, key):
    """
    GET /embed/<uuid:key>/
    Streams the latest TrackVersion’s file if the key is valid.
    """
    embed_key = get_object_or_404(EmbedKey, key=key)
    if embed_key.expires_at and embed_key.expires_at < datetime.now():
        return Response({"detail": "Embed key expired."}, status=status.HTTP_410_GONE)

    latest_version = (
        embed_key.track.versions.first() or embed_key.track
    )  # fall back to original file
    response = FileResponse(latest_version.audio_file.open("rb"), as_attachment=False)
    response["Content-Type"] = "audio/mpeg"
    response["X-Track-Title"] = embed_key.track.title
    response["X-Track-License"] = embed_key.track.license.spdx_id
    return response
