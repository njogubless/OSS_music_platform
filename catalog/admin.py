
from django.contrib import admin
from .models import Contributor, License, Track, TrackVersion, EmbedKey, Artist

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'url')
    search_fields = ('user__username', 'display_name')

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'spdx_id', 'url')
    search_fields = ('name', 'spdx_id')

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'license', 'is_public', 'created_at', 'genre')
    list_filter = ('is_public', 'license', 'genre')
    search_fields = ('title', 'description', 'uploader__display_name', 'uploader__user__username')
    raw_id_fields = ('uploader', 'license') 
    filter_horizontal = ('likes',) 

@admin.register(TrackVersion)
class TrackVersionAdmin(admin.ModelAdmin):
    list_display = ('track', 'version_label', 'created_at')
    list_filter = ('track',)
    search_fields = ('track__title', 'version_label')
    raw_id_fields = ('track',)

@admin.register(EmbedKey)
class EmbedKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'track', 'created_at', 'expires_at')
    list_filter = ('track',)
    search_fields = ('track__title', 'key')
    raw_id_fields = ('track',)

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)
    raw_id_fields = ('user',)