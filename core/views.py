from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Item, Order, OrderItem
from django.utils import timezone


# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "products.html", context)


def checkout(request):
    return render(request, "checkout.html")


class HomeView(ListView):
    model = Item
    template_name = 'home.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect('core:product', slug=slug)

# def home(request):

#     context = {
#         'items': Item.objects.all()
#     }

#     return render(request, "home.html")
