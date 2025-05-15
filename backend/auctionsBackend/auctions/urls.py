from django.urls import path
from .views import (
    AuctionListCreateView, AuctionDetailView,
    CategoryListCreateView, CategoryDetailView,
    BidListCreateView, BidDetailView,
    CommentListCreateView, CommentRetrieveUpdateDelete, 
    RatingCreateUpdateView, RatingDeleteView
)

app_name = "auctions"

urlpatterns = [
    path('', AuctionListCreateView.as_view(), name='auction-list-create'),
    path('<int:id_auction>/', AuctionDetailView.as_view(), name='auction-detail'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:id_category>/', CategoryDetailView.as_view(), name='category-detail'),
    path('<int:id_auction>/bids/', BidListCreateView.as_view(), name='bid-list-create'),
    path('<int:id_auction>/bids/<int:id_Bid>/', BidDetailView.as_view(), name='bid-detail'),
    path('<int:id_auction>/comments/', CommentListCreateView.as_view(), name='comment-create'),
    path('<int:id_auction>/comments/<int:pk>/', CommentRetrieveUpdateDelete.as_view(), name='comment-list-create-update'),
    path('<int:id_auction>/rate/', RatingCreateUpdateView.as_view(), name='rate-auction'),
    path('<int:id_auction>/rate/delete/', RatingDeleteView.as_view(), name='delete-rating'),
]