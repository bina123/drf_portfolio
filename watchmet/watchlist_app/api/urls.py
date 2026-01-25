from django.urls import path
from .views import WatchListAV, WatchListDetail, StreamPlatformList, StreamPlatformDetail, ReviewList, ReviewDetail

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchListDetail.as_view(), name='movie-detail'),
    path('streamplatforms/', StreamPlatformList.as_view(), name='stream-platforms'),
    path('streamplatforms/<int:pk>', StreamPlatformDetail.as_view(), name='stream-detail'),
    
    path('reviews/', ReviewList.as_view(), name="review-list"),
    path('reviews/<int:pk>', ReviewDetail.as_view(), name='review-detail')
]