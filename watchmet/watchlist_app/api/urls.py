from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (WatchListAV, WatchListDetail,WatchListGV, 
                    StreamPlatformViewset, 
                    ReviewList, ReviewDetail, ReviewCreate,
                    UserReview)

router = DefaultRouter()
router.register('streamplatforms',StreamPlatformViewset, basename="streamplatform" )

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('list-temp/', WatchListGV.as_view(), name='movie-list2'),
    path('<int:pk>/', WatchListDetail.as_view(), name='movie-detail'),
    path('', include(router.urls)),
    # path('streamplatforms/', StreamPlatformList.as_view(), name='stream-platforms'),
    # path('streamplatforms/<int:pk>', StreamPlatformDetail.as_view(), name='stream-detail'),
    
    # path('reviews/', ReviewList.as_view(), name="review-list"),
    # path('reviews/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name="review-create"),
    path('<int:pk>/reviews/', ReviewList.as_view(), name="review-list"),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name="review-detail"),
    path('user-review/', UserReview.as_view(), name="user-review"),
]