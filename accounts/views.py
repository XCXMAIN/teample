from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, serializers  # ← ✅ serializers 추가
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# ✅ 로그인
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={200: "로그인 성공", 401: "인증 실패"}
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

# ✅ 로그아웃
@swagger_auto_schema(
    method='post',
    responses={200: "로그아웃 완료"}
)
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': '로그아웃 완료'}, status=status.HTTP_200_OK)

# ✅ 회원가입 시리얼라이저
class RegisterSerializer(ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmPassword']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirmPassword')  # 저장 전에 제거
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

# ✅ 회원가입 뷰
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response(
                description="회원가입 성공",
                examples={"application/json": {
                    "username": "newuser",
                    "email": "newuser@example.com"
                }}
            ),
            400: "입력 오류"
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import numpy as np
import pandas as pd
import torch
import clip
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 실제 경로에 맞게 수정하세요 (예시)
EMB_PATH = os.path.join(BASE_DIR, 'data', 'clip_img_emb.npy')
META_PATH = os.path.join(BASE_DIR, 'data', 'clip_paths.csv')

# 임베딩 및 메타데이터 메모리 적재 (서버 기동 시 1회만)
img_embs = np.load(EMB_PATH)
meta_df = pd.read_csv(META_PATH)
img_embs = img_embs / np.linalg.norm(img_embs, axis=1, keepdims=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)
model.eval()

@api_view(['GET'])
@permission_classes([AllowAny])
def clip_search_view(request):
    query = request.GET.get('query', '')
    top_k = int(request.GET.get('top_k', 5))
    if not query:
        return Response({'error': '검색어(query)가 필요합니다.'}, status=400)

    N = img_embs.shape[0]
    if N == 0:
        return Response({'results': [], 'msg': '임베딩 데이터가 없습니다.'}, status=200)
    # top_k 값이 임베딩 개수보다 크면 top_k를 자동으로 맞춤
    if top_k > N:
        top_k = N

    # 텍스트 임베딩 생성
    text_tokens = clip.tokenize([query]).to(device)
    with torch.no_grad():
        text_emb = model.encode_text(text_tokens).cpu().numpy()[0]
    text_emb = text_emb / np.linalg.norm(text_emb)

    # 코사인 유사도 계산
    sims = img_embs @ text_emb
    idxs = np.argsort(-sims)[:top_k]

    results = []
    for i in idxs:
        results.append({
            'path': str(meta_df.iloc[i]['path']),
            'score': float(sims[i])
        })
    return Response({'results': results}, status=200)