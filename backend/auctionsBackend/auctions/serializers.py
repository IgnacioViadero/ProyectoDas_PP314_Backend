from rest_framework import serializers
from django.db.models import Avg
from .models import Category, Auction, Bid, Comment, Rating
from django.utils import timezone
from drf_spectacular.utils import extend_schema_field

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AuctionSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    auctioneer = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)

    isOpen = serializers.SerializerMethodField()


    class Meta:
        model = Auction
        fields = ['id', 'title', 'description', 'image', 'start_date', 'end_date',
                  'starting_price', 'stock', 'category', 'brand', 'rating', 'auctioneer',
                  'isOpen'                    
        ]
        read_only_fields = ['start_date']

    def get_rating(self, obj):
        ratings = obj.ratings.all()  # Usa related_name='ratings' del modelo Rating
        if ratings.exists():
            avg = ratings.aggregate(Avg('score'))['score__avg']
            return round(avg, 2)
        return 1  # Valor por defecto si no hay valoraciones
    
    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.end_date > timezone.now()
    
class RatingSerializer(serializers.ModelSerializer):
    auction = AuctionSerializer(read_only=True)
    class Meta:
        model = Rating
        fields = ['id', 'score', 'user', 'auction']
    
    def validate_score(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating entre 1 y 5")    
        return value


class AuctionMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'title', 'image']

class BidSerializer(serializers.ModelSerializer):
    subasta = AuctionMiniSerializer(read_only=True)
    bidder = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'subasta', 'cantidad', 'fecha', 'bidder']

class CommentSerializer(serializers.ModelSerializer):
    fecha_creacion = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    fecha_modificacion = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    user_comment = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user_comment', 'auction_comment', 'fecha_creacion', 'fecha_modificacion']

    def get_user_comment(self, obj):
        return {"username": obj.user_comment.username}