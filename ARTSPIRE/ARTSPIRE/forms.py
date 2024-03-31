from django import forms

from Artapp.models import Artwork, Auction, Bid


class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'category', 'aimg', 'Description', 'creationDate', 'width', 'height', 'frame', 'condition']

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['startDate', 'endDate', 'basePrice']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bidAmount']