from .models import CartItem

def cart_items_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        count = cart_items.count()
    else:
        count = 0

    return {'cart_items_count': count}
