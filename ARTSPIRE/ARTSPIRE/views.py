from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from ARTSPIRE.forms import ArtworkForm, AuctionForm, BidForm
from Artapp.models import Bid, Category, Artwork, Auction, User, Comment, Buyer, Seller
from django.contrib import auth
from django.conf import settings
from django.core.mail import send_mail

# Header and Footer pages
def Master(request):
    request.session['username']=request.session['username']
    return render(request, 'master.html')

def MasterSeller(request):
    request.session['username']=request.session['username']
    return render(request, 'masterSeller.html')
# End Header and Footer

#Login and signup
def Login_view(request):
    if request.method == 'POST':  
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password) 
        
        if user is not None:
            login(request, user)
            request.session['username']=username
            if user.user_type == 'Seller':
                return redirect('indexSeller') 
            else:
                return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')  
            return redirect('login_view') 
    else:
        return render(request, 'login.html')

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        user = User.objects.create_user(email=email, username=username, password=password, user_type=user_type)
        user.save()
        if user_type == 'Buyer':
            buyer = Buyer.objects.create(user=user)
            buyer.save()
        elif user_type == 'Seller':
            seller = Seller.objects.create(user=user)
            seller.save()
        return redirect('login_view')
    else:
        return render(request, 'signup.html')

def Logout(request):
    logout(request)
    request.session.flush()
    return redirect('login_view')

# End login and signup

#Buyer pages
def Index(request):
    if 'username' in request.session:
        request.session['username'] = request.session['username']
    category = Category.objects.all()
    context = {
        'category':category
    }
    return render(request, 'index.html', context)

def BrowseArt(request, id):
    if 'username' in request.session:
        request.session['username'] = request.session['username']
        if id == 0:
            artwork = Artwork.objects.all()
            auction = Auction.objects.all()
        else:
            category = get_object_or_404(Category, id=id)
            artwork = Artwork.objects.filter(category=category)
            auction = Auction.objects.all()
        artContext = {
            'artwork': artwork,
            'auction': auction
        }
        return render(request, 'browseArt.html', artContext)
    else:
        messages.warning(request, 'Login required.')
        return redirect('login_view')

def ArtworkDetail(request, id):
    request.session['username']=request.session['username']
    artworkDetail = get_object_or_404(Artwork, id=id)
    request.session['art']=artworkDetail.id
    auctionDetail = get_object_or_404(Auction, artwork=artworkDetail)
    if request.method == 'POST':
        comment_text = request.POST.get('message')
        comment = Comment(artwork=artworkDetail, user=request.user, commentText=comment_text, datePosted=timezone.now())
        comment.save()
        return redirect('artworkDetail', id=id)
    commentDetails = Comment.objects.filter(artwork=artworkDetail)
    return render(request, 'artworkDetail.html', {'artworkDetail': artworkDetail, 'auctionDetail': auctionDetail, 'commentDetails': commentDetails})

def BidArt(request, id):
    un=request.session['username']
    user = User.objects.get(email=un)
    buyer = Buyer.objects.get(user=user)
    artwork = Artwork.objects.get(id=id)
    auction = get_object_or_404(Auction, artwork=artwork)
    request.session['username']=un
    if request.method == 'POST':
        bidAmt=request.POST.get('bidamt')
        if auction.auctionStatus:
            if float(bidAmt) > auction.basePrice:
                bid=Bid(artwork=artwork, buyer=buyer, bidAmount=bidAmt)
                bid.save()
                return redirect('browseArt', id=0)
            else:
                messages.warning(request, 'Bid Amount should be greater than base amount.')
                return redirect('browseArt', id=0)
        else:
            messages.warning(request, 'Auction has been closed.')
            return redirect('browseArt', id=0)
    return render(request, 'bidForm.html', {'artwork': artwork}) 

def ViewMyBids(request):
    if 'username' in request.session:
        un=request.session['username']
        user = User.objects.get(email=un)
        buyer = Buyer.objects.get(user=user)
        request.session['username']=request.session['username']
        bids = Bid.objects.filter(buyer=buyer)
        return render(request, 'viewMyBids.html', {'bids': bids})
    else:
        messages.warning(request, 'Login required.')
        return redirect('login_view')

def DeleteBid(request,id):
    request.session['username']=request.session['username']
    bid = get_object_or_404(Bid, id=id)
    bid.delete()
    return redirect('viewMyBids')

def EditBid(request, id):
    request.session['username']=request.session['username']
    bid = get_object_or_404(Bid, id=id)
    if request.method == 'POST':
        form = BidForm(request.POST, instance=bid)
        if form.is_valid():
            form.save()
            return redirect('viewMyBids')
    else:
        form = BidForm(instance=bid)
    return render(request, 'editBid.html', {'form': form, 'bid': bid})

def Search(request):
    if 'username' in request.session:
        request.session['username']=request.session['username']
        if request.method == 'POST':
            search = request.POST.get('search_input')
            artworks = Artwork.objects.filter(title__icontains=search)
            if not artworks :
                users = User.objects.filter(username__icontains=search)
                sellers = Seller.objects.filter(user__in=users)
                artworks = Artwork.objects.filter(seller__in=sellers)
            if not artworks :
                messages.warning(request, "No results found")
                return redirect('index')
            
            context = {
                'artwork': artworks,
                'search': search,
            }
            return render(request, 'browseArt.html', context)
    else:
        messages.warning(request, 'Login required.')
        return redirect('login_view')

# End buyer functionality

#Seller functionality
def IndexSeller(request):
    request.session['username']=request.session['username']
    email = request.session.get('username')
    user = None
    if email:
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            pass
    
    context = {'user': user}
    return render(request, 'indexSeller.html', context)


def AddArt(request):
    request.session['username']=request.session['username']
    category = Category.objects.all()
    if request.method == "POST":
        artName=request.POST.get('title')
        artworkImage=request.FILES.get('artworkImage')
        desc=request.POST.get('description')
        cat=request.POST.get('category')
        cDate=request.POST.get('cDate')
        width=request.POST.get("width")
        height=request.POST.get("height")
        frame=request.POST.get("frame")
        condition=request.POST.get("condition")
        un=request.session['username']
        user = User.objects.get(email=un)
        seller = Seller.objects.filter(user=user).first()
        category = Category.objects.get(name=cat)
        en=Artwork(title=artName,category=category,aimg=artworkImage,Description=desc,creationDate=cDate,seller=seller, width=width, height=height, frame=frame, condition=condition)
        en.save()
        request.session['artsess']=en.id
        return render(request, 'auctionForm.html', {'artwork' : en})
    else:
        return render(request,'addArtwork.html', { 'categories' : category })


def AuctionArt(request, id):
    request.session['username']=request.session['username']
    artwork=request.session['artsess']
    if request.method == 'POST':
        artwork = get_object_or_404(Artwork, id=id)
        sDate=request.POST.get('sDate')
        eDate=request.POST.get('eDate')
        basePrice=request.POST.get('basePrice')
        auction=Auction(artwork=artwork, startDate=sDate, endDate=eDate, basePrice=basePrice, auctionStatus=True)
        auction.save()
        return render(request,'indexSeller.html')
    else:
        return render(request, 'auctionForm.html', {'artwork': artwork}) 
    
def ViewAllArtSeller(request):
    request.session['username']=request.session['username']
    un=request.session['username']
    user = User.objects.get(email=un)
    seller = Seller.objects.get(user=user)
    artworks = Artwork.objects.filter(seller=seller)
    return render(request, 'viewAllArtSeller.html', {'artwork': artworks})

def ArtworkDetailSeller(request, id):
    request.session['username']=request.session['username']
    artworkDetail = get_object_or_404(Artwork, id=id)
    request.session['art']=artworkDetail.id
    auctionDetail = get_object_or_404(Auction, artwork=artworkDetail)
    if request.method == 'POST':
        comment_text = request.POST.get('message')
        comment = Comment(artwork=artworkDetail, user=request.user, commentText=comment_text, datePosted=timezone.now())
        comment.save()
        return redirect('artworkDetailSeller', id=id)
    commentDetails = Comment.objects.filter(artwork=artworkDetail)
    return render(request, 'artworkDetailSeller.html', {'artworkDetail': artworkDetail, 'auctionDetail': auctionDetail, 'commentDetails': commentDetails})

def DeleteArtwork(request,id):
    request.session['username']=request.session['username']
    pi = get_object_or_404(Artwork, pk=id)
    pi.delete()
    return redirect('viewAllArtSeller')

def EditArtwork(request, id):
    request.session['username']=request.session['username']
    artwork = get_object_or_404(Artwork, id=id)
    if request.method == 'POST':
        form = ArtworkForm(request.POST, instance=artwork)
        if form.is_valid():
            form.save()
            return redirect('viewAllArtSeller')
    else:
        form = ArtworkForm(instance=artwork)
    return render(request, 'editArtwork.html', {'form': form, 'artwork': artwork})

def ViewAllAuctions(request):
    request.session['username']=request.session['username']
    un=request.session['username']
    user = User.objects.get(email=un)
    seller = Seller.objects.get(user=user)
    artworks= Artwork.objects.filter(seller=seller)
    auctions = Auction.objects.filter(artwork__in=artworks)
    return render(request, 'viewAllAuctions.html', {'auctions': auctions})

def EditAuction(request, id):
    request.session['username']=request.session['username']
    auction = get_object_or_404(Auction, id=id)
    if request.method == 'POST':
        form = AuctionForm(request.POST, instance=auction)
        if form.is_valid():
            form.save()
            return redirect('viewAllAuctions')
    else:
        form = AuctionForm(instance=auction)
    return render(request, 'editAuction.html', {'form': form, 'auction': auction})


def SearchSeller(request):
    if 'username' in request.session:
        request.session['username']=request.session['username']
        if request.method == 'POST':
            search = request.POST.get('search_input')
            un=request.session['username']
            user = User.objects.get(email=un)
            seller = Seller.objects.get(user=user)
            artworks = Artwork.objects.filter(title__icontains=search, seller=seller)
            if not artworks :
                messages.warning(request, "No results found")
                return redirect('indexSeller')
            
            context = {
                'artwork': artworks,    
                'search': search,
            }
            return render(request, 'viewAllArtSeller.html', context)

# End seller fucntionality

# Auction functions
def GenerateAuctionResult(request, id):
    request.session['username']=request.session['username']
    un=request.session['username']
    user = User.objects.get(email=un)
    artwork = get_object_or_404(Artwork, id=id)
    auction = get_object_or_404(Auction, artwork=artwork)
    if auction.endDate <= timezone.now():
        if not auction.winner:
            winning_bid = Bid.objects.filter(artwork=artwork).order_by('-bidAmount').first()
            if winning_bid:
                auction.winner = winning_bid.buyer
                auction.auctionStatus=False
                auction.save()
                artwork.artworkStatus=False
                artwork.save()
                return render(request, 'auctionResult.html', {'auction': auction, 'artwork': artwork, 'user':user})
            else:
                messages.warning(request, 'No winning bid found.')
                return redirect('viewMyBids')
        else:
            return render(request, 'auctionResult.html', {'auction': auction, 'artwork': artwork, 'user':user})
    else:
        messages.warning(request, 'Auction end time has not passed yet.')
        return redirect('viewMyBids')

def SendWinnerEmail(request, id) :
    request.session['username']=request.session['username']
    if request.method == 'POST':
        name=request.POST.get("name")
        email=request.POST.get("email")
        title=request.POST.get("title")
        user = get_object_or_404(User, id=id)
        subject = 'Congratulations You Have Won the Auction'
        message = f'''Dear {name},
        Congratulations! We are thrilled to inform you that you have won the auction for the artwork titled {title}.
        Your bid was the highest, and as a result, you have been declared the winner of the auction. We would like to extend our warmest congratulations on your successful bid.
        Here are the details of your winning bid:
        To proceed with the next steps, please contact us at {user.email} within the next 15 days to arrange for payment and shipping details.
        Once again, congratulations on your win! We hope you enjoy your new artwork.
        Best regards,
        ARTSPIRE'''
        email_from = 'artspire412official@gmail.com'
        send_mail( subject, message, email_from, [email])
        return redirect('viewMyBids')
    return redirect('viewMyBids')

# End auction functionality