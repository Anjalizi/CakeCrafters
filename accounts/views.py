from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def signup(request):
	if request.method=='POST':
		if request.POST['password1'] == request.POST['password2']:
			# check if the username has already been taken
			try:
				user = User.objects.get(username=request.POST['username'])
				return render(request, 'accounts/signup.html', {'error' : "Username has already been taken"})
			except User.DoesNotExist:
				user = User.objects.create_user(
					username=request.POST['username'], 
					password=request.POST['password1'],
					email=request.POST['email'])
				# logging in as the user who signed up, can't access admin page now
				# login(request, user) 
				return render(request, 'accounts/signup.html', {'error' : "New User created"})
		else:
			return render(request, 'accounts/signup.html', {'error' : "Paswords didn't match"})
	else:
		return render(request, 'accounts/signup.html')

def login_view(request):
	if request.method=='POST':
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			login(request, user)
			# since it is not a permanent field in the form, created only when there is 'next'
			if 'next' in request.POST:
				return redirect(request.POST['next'])
			return redirect('index')
		else:
			return render(request, 'accounts/login.html', {'error' : "Account does not exist OR Username and Password didn't match"})
	else:
		return render(request, 'accounts/login.html')

def logout_view(request):
	if request.method == 'POST':
		logout(request)
		return redirect('index')