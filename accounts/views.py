from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from saffron.views import index


def user_login(request):
    if request.method == 'POST':
        print('let\'s login !')
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            print('user is ok !')
            login(request, user)
            return render(request, 'website/index.html')
    print('lets render to login')
    return render(request, 'accounts/login.html')