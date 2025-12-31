
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken import views as drf_auth_views
from django.conf.urls.static import static

# Import corporate routers
from skyport import urls as corporate_urls

urlpatterns = [
     # -----------------------------
    # Django Admin
    # -----------------------------
    path('admin/', admin.site.urls),

    # -----------------------------
    # Authentication (DRF Token)
    # -----------------------------
    # path('api-token-auth/', drf_auth_views.obtain_auth_token, name='api-token-auth'),
     # Auth (Djoser)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # -----------------------------
    # Corporate API
    # -----------------------------
    path('api/', include(corporate_urls)),

    # -----------------------------
    # API Documentation (OpenAPI)
    # -----------------------------
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
