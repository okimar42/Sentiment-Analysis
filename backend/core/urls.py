"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.authtoken import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from sentiment_analysis.views import UserRegistrationView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("sentiment_analysis.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api-token-auth/", auth_views.obtain_auth_token),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/register/", UserRegistrationView.as_view(), name="user-register"),
]

if settings.DEBUG:
    import debug_toolbar
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )

    urlpatterns = [
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
