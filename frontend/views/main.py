from django.shortcuts import render
from django.http import JsonResponse

def home_view(request):
    return render(request, 'home.html')

def health(request):
    return JsonResponse({
        "success": True,
        "message": "site is working"
    }, status=200)