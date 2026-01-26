from watchlist_app.models import WatchList, StreamPlatform, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
# from rest_framework import mixins
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly 
from .permissions import IsAdminOrReadonly, IsReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from .throttling import ReviewDetailThrottle, ReviewListThrottle

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        watchlist = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You can not review more than once on single watch!")
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2
        
        watchlist.number_rating += 1
        watchlist.save()
        
        serializer.save(watchlist=watchlist, review_user=review_user)

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadonly]
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
        
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchListDetail(APIView):
    permission_classes = [IsAdminOrReadonly]
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(movie)
            return Response(serializer.data)
        except WatchList.DoesNotExist:
            return Response({'error': 'Model Does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class StreamPlatformViewset(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadonly]
    
# class StreamPlatformViewset(viewsets.ViewSet):
    
#     def list(self, request):
#         streamplatform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(streamplatform, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
        
# class StreamPlatformList(APIView):
#     def get(self, request):
#         streamplatforms = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(streamplatforms, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         seriallizer = StreamPlatformSerializer(data=request.data)
#         if seriallizer.is_valid():
#             seriallizer.save()
#             return Response(seriallizer.data)
#         return Response(seriallizer.errors)      
    
# class StreamPlatformDetail(APIView): 
#     def get(self, request, pk):
#         try:
#             streamplatform = StreamPlatform.objects.get(pk=pk)
#             serializer = StreamPlatformSerializer(streamplatform)
#             return Response(serializer.data)
#         except StreamPlatform.DoesNotExist:
#             return Response({"error": 'Model does not exists!!'}, status=status.HTTP_400_BAD_REQUEST)
        
#     def put(self, request, pk):
#         try:
#             streamplatform = StreamPlatform.objects.get(pk=pk)
#             serializer = StreamPlatformSerializer(streamplatform, data = request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors)
#         except StreamPlatform.DoesNotExist:
#             return Response({"error":"Model does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, pk):
#         streamplatform = StreamPlatform.objects.get(pk=pk)
#         streamplatform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)   

# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response({'movies': serializer.data})
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT','DELETE'])
# def movie_detail(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#             serializer = MovieSerializer(movie)
#             return Response(serializer.data)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Model not found'},status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)