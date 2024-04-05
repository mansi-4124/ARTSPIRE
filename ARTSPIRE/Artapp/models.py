from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django_resized import ResizedImageField

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10)

    # Required fields for AbstractBaseUser
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_type']

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='artapp_user_groups',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='artapp_user_permissions',
        related_query_name='user'
    )
    
    def __str__(self):
        return self.username


class Seller(models.Model):
    totalSales = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    successAuctions = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = ResizedImageField(size=[300, 300], crop=['middle', 'center'])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Artwork(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    aimg = ResizedImageField(size=[262, 280], default='/static/img/default-artwork.jpg')
    Description = models.TextField()
    creationDate = models.DateField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='artworks_seller')
    artworkStatus = models.BooleanField(null=False, default=True)
    width = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    frame = models.CharField(max_length=30, default='No')
    condition = models.CharField(max_length=50, default='Good')
    def __str__(self):
        return self.title

class Buyer(models.Model):
    favourites = models.ForeignKey(Artwork, on_delete=models.CASCADE, null=True)
    totalBids = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Auction(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    basePrice = models.DecimalField(max_digits=10, decimal_places=2)
    auctionStatus = models.BooleanField()
    winner=models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)
    


class Bid(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='bids_buyer')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    bidAmount = models.DecimalField(max_digits=10, decimal_places=2)


class Comment(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    datePosted = models.DateTimeField()