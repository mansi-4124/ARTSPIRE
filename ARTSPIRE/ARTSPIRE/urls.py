"""
URL configuration for ARTSPIRE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('master', views.Master, name='master'),
    path('masterSeller', views.MasterSeller, name='masterSeller'),
    path('', views.Index, name='index'),

    path('login/', views.Login_view, name='login_view'),
    path('signup/', views.Signup, name='signup'),
    path('logout/', views.Logout, name='logout'),

    path('browseArt/<int:id>/', views.BrowseArt, name='browseArt'),
    path('artworkDetail/<int:id>/', views.ArtworkDetail, name='artworkDetail'),
    path('editBid/<int:id>/', views.EditBid, name='editBid'),
    path('deleteBid/<int:id>/', views.DeleteBid, name='deleteBid'),
    path('viewMyBids/', views.ViewMyBids, name='viewMyBids'),
    path('search/', views.Search, name='search'),
    path('bidArt/<int:id>/', views.BidArt, name='bidArt'),

    path('auctionArt/<int:id>/', views.AuctionArt, name='auctionArt'),
    path('addArt/', views.AddArt, name='addArt'),
    path('indexseller/', views.IndexSeller, name='indexSeller'),
    path('deleteArtwork/<int:id>/', views.DeleteArtwork, name='deleteArtwork'),
    path('artworkDetailSeller/<int:id>/', views.ArtworkDetailSeller, name='artworkDetailSeller'),
    path('viewAllArtSeller/', views.ViewAllArtSeller, name='viewAllArtSeller'),
    path('viewAllAuctions/', views.ViewAllAuctions, name='viewAllAuctions'),
    path('editArtwork/<int:id>/', views.EditArtwork, name='editArtwork'),
    path('editAuction/<int:id>/', views.EditAuction, name='editAuction'),
    path('searchSeller/', views.SearchSeller, name='searchSeller'),    

    path('generateAuctionResult/<int:id>/', views.GenerateAuctionResult, name='generateAuctionResult'),
    path('sendWinnerEmail/<int:id>/', views.SendWinnerEmail, name='sendWinnerEmail'),

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)