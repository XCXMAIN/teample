from django.shortcuts import render
from django.http import JsonResponse
from .models import search_images
from .utils import get_image_paths

def clip_search_view(request):
    query = request.GET.get('text', '')
    top_k = int(request.GET.get('top_k', 5))

    image_paths = get_image_paths()
    results = search_images(query, image_paths, top_k)

    return JsonResponse({'results': results})
