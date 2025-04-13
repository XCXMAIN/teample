from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import logout


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    responses={
        200: openapi.Response(
            description="로그인 성공",
            examples={
                "application/json": {
                    "access": "access_token값",
                    "refresh": "refresh_token값"
                }
            }
        ),
        401: "로그인 실패 (인증 실패)"
    }
)
@api_view(['POST'])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def logout_view(request):
    """
    JWT 로그아웃 (서버단 로그아웃 처리 예시)
    """
    logout(request)  # Django 세션 로그아웃 (JWT에서는 실제 세션은 없지만 보안상 추가)
    return Response({'message': '로그아웃 완료'}, status=status.HTTP_200_OK)