from django.contrib import admin

# Register your models here.
from .models import User,Seller,Artwork,Buyer,Auction,Bid,Category, Comment

admin.site.register(User)
admin.site.register(Seller)
admin.site.register(Artwork)
admin.site.register(Buyer)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Comment)