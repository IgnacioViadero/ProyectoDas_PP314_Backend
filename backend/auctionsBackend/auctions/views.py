# auctions/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Q, Avg
from .models import Auction, Category, Bid, Comment, Rating
from .serializers import AuctionSerializer, CategorySerializer, BidSerializer, CommentSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class AuctionListCreateView(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    #permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = Auction.objects.all()
        texto = self.request.query_params.get('texto', None)
        categoria = self.request.query_params.get('categoria', None)
        rating_min = self.request.query_params.get('ratingMin', None)
        precio_min = self.request.query_params.get('precioMin', None)
        precio_max = self.request.query_params.get('precioMax', None)

        queryset = queryset.annotate(
            avg_rating=Avg('ratings__score')  # Usa related_name='ratings' del modelo Rating
        )

        if texto:
            queryset = queryset.filter(
                Q(title__icontains=texto) | Q(description__icontains=texto)
            )
        if categoria:
            queryset = queryset.filter(category__id=categoria)

        if rating_min:
            queryset = queryset.filter(avg_rating__gte=float(rating_min))

        if precio_min and precio_max:
            queryset = queryset.filter(
                starting_price__gte=precio_min,
                starting_price__lte=precio_max   
            )
        elif precio_max: 
            queryset = queryset.filter(starting_price__lte=precio_max)
        elif precio_min:  
            queryset = queryset.filter(starting_price__gte=precio_min)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(auctioneer=self.request.user)

    

class AuctionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    lookup_url_kwarg = 'id_auction'
    def perform_update(self, serializer):
        # Verifica que el usuario sea el propietario antes de actualizar
        if self.get_object().auctioneer != self.request.user:
            raise PermissionDenied("Solo el propietario de la subasta puede editarla.")
        serializer.save()

    def perform_destroy(self, instance):
        # Verifica que el usuario sea el propietario antes de eliminar
        if instance.auctioneer != self.request.user:
            raise PermissionDenied("Solo el propietario de la subasta puede eliminarla.")
        instance.delete()
    

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = 'id_category'

class BidListCreateView(generics.ListCreateAPIView):
    serializer_class = BidSerializer

    def get_queryset(self):
        id_auction = self.kwargs['id_auction']
        return Bid.objects.filter(subasta_id=id_auction)

    def perform_create(self, serializer):
        id_auction = self.kwargs['id_auction']
        auction = Auction.objects.get(id=id_auction)
        serializer.save(subasta=auction, bidder=self.request.user)

class BidDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BidSerializer
    lookup_url_kwarg = 'id_Bid'
    def get_queryset(self):
        id_auction = self.kwargs['id_auction']
        return Bid.objects.filter(subasta_id=id_auction) 

class CommentListCreateView(generics.ListCreateAPIView): 
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    def get_queryset(self):
        return Comment.objects.filter(auction_comment_id=self.kwargs["id_auction"])
    def perform_create(self, serializer):
        serializer.save(user_comment=self.request.user, auction_comment_id=self.kwargs["id_auction"])

class CommentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView): 
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer 
    def get_queryset(self):
        return Comment.objects.filter(user_comment=self.request.user)
    def perform_update(self, serializer):
        if self.get_object().user_comment != self.request.user:
            raise PermissionDenied("No puedes editar comentarios de otros usuarios.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user_comment != self.request.user:
            raise PermissionDenied("No puedes eliminar comentarios de otros usuarios.")
        instance.delete()


class RatingCreateUpdateView(generics.GenericAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, id_auction):
        auction = generics.get_object_or_404(Auction, id=id_auction)
        rating, created = Rating.objects.get_or_create(
            user=request.user,
            auction=auction,
            defaults={'score': request.data.get('score')}
        )
        if not created:
            rating.score = request.data.get('score')
            rating.save()
        serializer = self.get_serializer(rating)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

class RatingDeleteView(generics.DestroyAPIView):
    queryset = Rating.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return generics.get_object_or_404(
            self.get_queryset(),
            user=self.request.user,
            auction_id=self.kwargs['id_auction']
        )    