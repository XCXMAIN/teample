# import numpy as np
# import pandas as pd
# import torch
# import clip
# import os

# ======== CLIP 이미지 검색 (임시 더미) ========

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# EMB_PATH = os.path.join(BASE_DIR, 'data', 'clip_img_emb.npy')
# META_PATH = os.path.join(BASE_DIR, 'data', 'clip_paths.csv')

# img_embs = np.load(EMB_PATH)
# meta_df = pd.read_csv(META_PATH)
# img_embs = img_embs / np.linalg.norm(img_embs, axis=1, keepdims=True)

# device = "cuda" if torch.cuda.is_available() else "cpu"
# model, preprocess = clip.load("ViT-L/14", device=device)
# model.eval()

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('query', openapi.IN_QUERY, description="검색어", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('top_k', openapi.IN_QUERY, description="최대 반환 개수", type=openapi.TYPE_INTEGER, required=False, default=5)
    ],
    responses={200: openapi.Response(
        description="검색 결과 예시",
        examples={"application/json": {
            "results": [
                {"path": "frame_0.png", "score": 0.82}
            ]
        }}
    )}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def clip_search_view(request):
    # 실제 모델 로직 주석!
    # query = request.GET.get('query', '')
    # top_k = int(request.GET.get('top_k', 5))
    # if not query:
    #     return Response({'error': '검색어(query)가 필요합니다.'}, status=400)

    # N = img_embs.shape[0]
    # if N == 0:
    #     return Response({'results': [], 'msg': '임베딩 데이터가 없습니다.'}, status=200)
    # if top_k > N:
    #     top_k = N

    # text_tokens = clip.tokenize([query]).to(device)
    # with torch.no_grad():
    #     text_emb = model.encode_text(text_tokens).cpu().numpy()[0]
    # text_emb = text_emb / np.linalg.norm(text_emb)

    # sims = img_embs @ text_emb
    # idxs = np.argsort(-sims)[:top_k]

    # results = []
    # for i in idxs:
    #     results.append({
    #         'path': str(meta_df.iloc[i]['path']),
    #         'score': float(sims[i])
    #     })
    # return Response({'results': results}, status=200)

    # 임시 더미 결과만 리턴
    return Response({'results': [
        {'path': 'dummy_image.jpg', 'score': 1.0}
    ]}, status=200)
