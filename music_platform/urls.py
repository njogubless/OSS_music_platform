
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from catalog.views import TrackViewSet, TrackVersionViewSet, LicenseViewSet, embed_stream

router = routers.DefaultRouter()
router.register(r"tracks", TrackViewSet)
router.register(r"versions", TrackVersionViewSet)
router.register(r"licenses", LicenseViewSet)

schema_view = get_schema_view(
    openapi.Info(title="Music API", default_version="v1"),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("embed/<uuid:key>/", embed_stream, name="embed-stream"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
