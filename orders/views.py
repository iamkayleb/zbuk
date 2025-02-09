from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
from carts.models import CartItem
from ebookstore import settings
from orders.models import Order, OrderItem

# Create your views here.

def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_completed.html')