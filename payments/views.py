from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from products.models import ActiveCart
from .models import Transaction
from django.contrib.auth.decorators import login_required
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt

@login_required
def initiate_payment(request):
	cart_items = ActiveCart.objects.filter(buyer=request.user)
	amount = 0
	for obj in cart_items:
		amount += (obj.item.cost * obj.quantity)
	if request.method == "POST": 
		transaction = Transaction.objects.create(made_by=request.user, amount=amount)
		transaction.save()
		merchant_key = settings.PAYTM_SECRET_KEY

		params = (
			('MID', settings.PAYTM_MERCHANT_ID),
			('ORDER_ID', str(transaction.order_id)),
			('CUST_ID', str(transaction.made_by.email)),
			('TXN_AMOUNT', str(transaction.amount)),
			('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
			('WEBSITE', settings.PAYTM_WEBSITE),
			('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
			('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
		)

		paytm_params = dict(params)
		checksum = generate_checksum(paytm_params, merchant_key)

		transaction.checksum = checksum
		transaction.save()

		paytm_params['CHECKSUMHASH'] = checksum
		print('SENT: ', checksum)
		return render(request, 'payments/redirect.html', context=paytm_params)
	else:
		return render(request, 'payments/pay.html', {'amount':amount})	

@csrf_exempt
def callback(request):
	if request.method == 'POST':
		received_data = dict(request.POST)
		paytm_params = {}
		paytm_checksum = received_data['CHECKSUMHASH'][0]
		for key, value in received_data.items():
			if key == 'CHECKSUMHASH':
				paytm_checksum = value[0]
			else:
				paytm_params[key] = str(value[0])
		# Verify checksum
		is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
		if is_valid_checksum:
			received_data['message'] = "Checksum Matched"
		else:
			received_data['message'] = "Checksum Mismatched"
		return render(request, 'payments/callback.html', context=received_data)
