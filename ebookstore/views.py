from django.shortcuts import redirect, render
from store.models import Book

def home(request):
    books = Book.objects.filter(is_featured=True).order_by('-created_date')
    context = {
        'books': books
    }
    return render(request, 'index.html', context)


    current_user = request.user

    cart_items = OrderItem.objects.filter(user=current_user, ordered=False)
    cart_count = cart_items.count()

    if not cart_items.exists():
        return redirect('cart')

    # for cart_item in cart_items:
    #     total += (cart_item.book.price * cart_item.quantity)

    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        order_total = sum(cart_item.book.price * cart_item.quantity for cart_item in cart_items)

        order = Order.objects.get(user=current_user, is_ordered=False)

         # Save the order
        order = Order.objects.create(
            user=current_user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            order_total=order_total
        )

        cart_items.update(order=order, ordered=True)
        for cart_item in cart_items:
            cart_item.ordered = True,
            cart_item.order = order,
            cart_item.save()

        context = {
            'order': order,
            'cart_items': cart_items,
            'order_total': order_total,
        }
        return redirect("checkout")
    return render(request, 'checkout.html', context)