from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import News, SavedNews
from rest_framework.response import Response
from .serializers import NewsSerializer
from rest_framework.decorators import api_view

# Create your views here.

def app_view(request):
    city = request.GET.get('city')
    search = request.GET.get('search')
    
    news = News.objects.all()

    if city:
        news = news.filter(location__iexact=city)
    
    if search:
        news = news.filter(title__icontains=search) | news.filter(desc__icontains=search)

    return render(request, 'news.html', {'news': news})

def  news_detail(request,news_id):
    single_news = News.objects.get(id=news_id)
    return render(request, 'news_detail.html', {'n': single_news})

def user_login(request):
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')

@login_required
def create_news_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        location = request.POST.get('location')
        News.objects.create(
            title=title,
            desc=desc,
            location=location,
        )
        return redirect('/')
    return render(request, 'create_news.html')


def user_logout(request):
    logout(request)
    return redirect('/login/')


@login_required
def save_news(request, news_id):
    news = News.objects.get(id=news_id)
    SavedNews.objects.get_or_create(user=request.user, news=news)
    return redirect('/')


@login_required
def saved_news(request):
    data = SavedNews.objects.filter(user=request.user)
    return render(request, 'saved_news.html', {'data': data})

@login_required
def remove_saved_news(request, saved_news_id):
    saved_news = SavedNews.objects.get(id=saved_news_id, user=request.user)
    saved_news.delete()
    return redirect('/saved-news/')

@api_view(['GET'])
def news_list_api(request):
    news = News.objects.all()
    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_news_api(request):
    serializer = NewsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)