from django.db import models
from users.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Auction(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='', null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    auctioneer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='my_auctions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    

class Bid(models.Model):
    subasta = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='pujas')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='my_bids')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subasta} - {self.cantidad}"

class Comment(models.Model): 
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    user_comment = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    auction_comment = models.ForeignKey(Auction,on_delete=models.CASCADE)

    class Meta: 
        ordering = ('id',)
    
    def __str__(self): 
        return f'The comment: {self.title}, with description: {self.description} from user: {self.user_comment}'
    
class Rating(models.Model):
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='ratings')

    class Meta:
        unique_together = ('user', 'auction')
        ordering = ('id',)

    def __str__(self):
        return f"{self.user.username} rated {self.auction.title} with {self.score}"