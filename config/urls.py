from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.shortcuts import redirect
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# ✅ Swagger 보안 스키마 설정
schema_view = get_schema_view(
   openapi.Info(
      title="My Django API",
      default_version='v1',
      description="API 문서입니다.",
      contact=openapi.Contact(email="your@email.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   # 🔽 여기 추가
   authentication_classes=[],  # 또는 생략 가능
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', lambda request: redirect('schema-swagger-ui')),
]
