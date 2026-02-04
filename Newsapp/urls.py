from django.urls import path
from Newsapp import views
from Newsapp.views import news_list_api, create_news_api
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.app_view, name="app"),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('save-news/<int:news_id>/', views.save_news, name='save_news'),
    path('saved-news/', views.saved_news, name='saved_news'),
    path('remove-saved-news/<int:saved_news_id>/', views.remove_saved_news, name='remove_saved_news'),
    path('create-news/', views.create_news_view, name='create_news'),
    path('api/news/', news_list_api),
    path('api/news/create/', create_news_api),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]