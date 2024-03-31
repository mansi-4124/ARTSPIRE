from django.contrib import admin

# Register your models here.
from .models import User,Admin,Seller,Artwork,Buyer,Auction,Bid,Purchase, Category, Comment

admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Seller)
admin.site.register(Artwork)
admin.site.register(Buyer)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Purchase)
admin.site.register(Category)
admin.site.register(Comment)