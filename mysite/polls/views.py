# polls/views.py

from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import CustomUser

# Create your views here.
def index(request):
    content = {'login':'accounts/login', 'login2':'accounts/login2', 
               'login3':'accounts/login3', 'logout':'accounts/logout',
            'register':'accounts/register', 'accounts':'accounts/'}
    #세션이 존재하면 db에서 값 추출
    if request.session.get('user'):
        user = CustomUser.objects.filter(email = request.session.get('user'))
        print(user.first().name)
        pwd = user.first().password
        user_dict = {'pwd':pwd}
        content = {**content, **user_dict} #딕셔너리 병합
        print(request.session.keys())
    return render(request,'polls/index.html', content)