from django.shortcuts import render, redirect
import requests
from store.models import Book
from .models import CartItem, Cart
from orders.models import Order, OrderItem
from django.conf import settings
# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
        print("Session key does not exist, will be created")
    else:
        print("Session key already exists")
    return cart
def cart(request, quantity=0, total=0, cart_items=None):
    try:
        sub_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.book.price * cart_item.quantity)
            quantity += cart_item.quantity
        sub_total = total
        cart_count = cart_items.count()
    except:
        pass
    context = {
            'quantity': quantity,
            'total': sub_total,
            'cart_items': cart_items,
            # 'cart_count': cart_count
    }
    return render(request, 'shop-cart.html', context)

def add_cart(request, book_id):
    current_user = request.user
    book = Book.objects.get(id=book_id)
    try:
        if current_user.is_authenticated:
            is_cart_item_exist = CartItem.objects.filter(user=current_user, book=book).exists()
            if is_cart_item_exist:
                cart_item = CartItem.objects.get(user=current_user, book=book)
                
            else:
                cart_item = CartItem.objects.create(
                    user=current_user,
                    book=book,
                    quantity=1,
                )
            if cart_item.quantity >= 1:
                cart_item.quantity += 1
                cart_item.save()
            else:
                pass
        
            
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            is_cart_item_exist = CartItem.objects.filter(cart=cart, book=book).exists()
            if is_cart_item_exist:
                cart_item = CartItem.objects.get(cart=cart, book=book)
            else:
                cart_item = CartItem.objects.create(
                    cart=cart,
                    book=book,
                    quantity=1,
                )
            if cart_item.quantity >= 1:
                cart_item.quantity += 1
                cart_item.save()
           
    except:
        pass
    
    return redirect('cart')
def remove_cart(request, book_id, cart_item_id):
    book = Book.objects.get(id=book_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, book=book, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(cart=cart, book=book)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    
    return redirect('cart')

def remove_cart_item(request, book_id, cart_item_id):
    book = Book.objects.get(id=book_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, book=book, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(cart=cart, book=book)
        cart_item.delete()
    except:
        pass
    return redirect('cart')

def checkout(request):
    current_user = request.user
    
    cart_items = CartItem.objects.filter(user=current_user)
    print(cart_items)
    cart_count = cart_items.count()

    order_total = sum(cart_item.book.price * cart_item.quantity for cart_item in cart_items)

    context = {
        'cart_items': cart_items,
        'order_total': order_total,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        'email': current_user.email,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
    }
     
    if request.method == 'POST':
        reference = request.POST.get('reference')

    
        url="https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }

        response = requests.get(url, headers=headers)
        response_data = response.json()
        print("Response data:", response_data)
        if response_data.get('status') and response_data['data']['status'] == 'success':
            try:
                order = Order.objects.create(
                    user = current_user,
                    total_amount = order_total,
                    transaction_id = reference, 
                    status = 'completed'
                )
                print('order was created, {order}')
            except Exception as e:
                print('Order was not created {e}')
            cart_items.delete()
            
            return redirect('store')
      

    return render(request, 'checkout.html', context)
    
