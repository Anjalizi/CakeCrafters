from django.shortcuts import render, redirect
from .models import Product, ActiveCart
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index(request):
	# for shopbox homepage
    return render(request, 'products/index.html')

@login_required
def home(request):
	products = Product.objects.order_by('cost')
	return render(request, 'products/home.html', {'all_products':products})

@login_required
def cart(request, pk):
	cart_items = ActiveCart.objects.filter(buyer__id=pk)
	total_cost = 0
	for obj in cart_items:
		total_cost += (obj.item.cost * obj.quantity)
	return render(request, 'products/cart.html', {'all_items':cart_items, 'total_cost':total_cost})

@login_required
def category1(request):
	# cost is less than or equal to 200
	cat1_products = Product.objects.filter(cost__lte=200).order_by('cost')
	return render(request, 'products/home.html', {'all_products':cat1_products})

@login_required
def category2(request):
	# cost is greater than 200 and less than equal to 400
	q1 = Product.objects.filter(cost__gt=200)
	q2 = Product.objects.filter(cost__lte=400)
	cat2_products = q1.intersection(q2).order_by('cost')
	return render(request, 'products/home.html', {'all_products':cat2_products})

@login_required
def add2cart(request, pk, pid):
	product = Product.objects.get(pk=pid)
	buyer = User.objects.get(pk=pk)
	try:
		cart_item = ActiveCart.objects.get(item=product, buyer=buyer)
		cart_item.quantity += 1
	except ObjectDoesNotExist:
		cart_item = ActiveCart.objects.create(item=product, buyer=buyer, quantity=1)
	cart_item.save()
	return redirect('products:cart', pk=pk)

@login_required
def removeFromCart(request, pk, pid):
	product = Product.objects.get(pk=pid)
	cart_item = ActiveCart.objects.get(item=product, buyer=User.objects.get(pk=pk))
	cart_item.quantity -= 1
	cart_item.save()
	if(cart_item.quantity == 0):
		ActiveCart.objects.filter(item=product, buyer=User.objects.get(pk=pk)).delete()
	return redirect('products:cart', pk=pk)

@login_required
def checkout(request):
	return render(request, 'products/checkout.html')





