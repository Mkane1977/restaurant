from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Restaurant, Menu, Order

def place_order(request):
    if request.method == 'POST':
        customer = request.user
        cart = request.session.get('cart', {})
        
        # Create the order
        order = Order.objects.create(customer=customer)
        
        # Create order items
        for menu_id, cart_item in cart.items():
            menu = get_object_or_404(Menu, id=int(menu_id))
            quantity = cart_item['quantity']
            order_item = order.items.create(menu=menu, quantity=quantity)
        
        # Clear the cart
        del request.session['cart']
        
        # Send notifications
        send_order_notification_to_restaurant(order)
        send_order_confirmation_to_customer(order)
        
        # Update order status
        order.status = 'pending'
        order.save()
        
        messages.success(request, 'Your order has been placed successfully.')
        return redirect('order_confirmation')
    
    return render(request, 'place_order.html')
