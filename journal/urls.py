from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('new/', views.NewPostView.as_view(), name='new_post'),
    path('thanks/', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),

]