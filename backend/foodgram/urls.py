from django.contrib import admin
from django.urls import include, path

from foodgram import settings

urlpatterns = [
    path("api/", include("api.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
