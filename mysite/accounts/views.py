from django.shortcuts import render, redirect
from django.contrib import auth
from .models import CustomUser
from django.contrib import messages
from django.db import connection
# Create your views here.

def home(request):
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'accounts/home.html',context)

def register(request):
		# 회원가입 성공 시 redirect 할 url 지정
    url = 'accounts:home'
    # request 메소드가 post로 오는지 확인, get이면 else문 실행
    if request.method == "POST":
		    # email, name, password1로 전송된 값을 변수에 담아준다.
        email = request.POST['email']
        name = request.POST['name']
        password1 = request.POST['password1']
        
        # 중복되는 email-user가 존재하는지 확인
        user = CustomUser.objects.filter(email = email)
        
        # 중복되는 email-user가 없다면 len값은 0
        if len(user) == 0:
		        # 중복되는 email-user가 없다면 DB에 입력값 저장
            CustomUser.objects.create_user(
                username=email,
                email=email,  
                name=name,  
                password=password1
            )            
        else:
		        # 중복되는 ID가 존재할 시 alert.html를 호출함과 동시에 
		        # 메시지와 location 할 url값을 넘겨준다.
            alert = {'msg':'중복된 아이디 입니다.', 'url':'register'}
            return render(request, 'alert.html', {'msg' : alert})    

				# 해당되는 url로 redirect
        return redirect(url)
    else:
		    #request 메소드가 get으로 오면 회원가입 페이지를 보여준다.
        return render(request, 'accounts/register.html')
    
# orm기법
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 로그인 과정 없이 단순히 값만 넘김
        context = {
            'email': email,
            'password': password
        }
        
        return render(request, 'polls/index.html', context)

    return render(request, 'accounts/login.html')

# RawQuery 기법
def login2(request):
		# 회원가입 성공 시 redirect 할 url 지정
    url = "polls:index"
    # 에러 유무를 구분하기 위한 변수
    alert = ""
    # request 메소드가 post로 오는지 확인, get이면 else문 실행
    if request.method == 'POST':
		    # email, password1로 전송된 값을 변수에 담아준다.
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email is not None and password is not None:
		    # RowQuery를 Exctue할 cursor 등록
            cursor = connection.cursor()
            
            # 쿼리문 작성 -> email이 일치하는 레코드의 Password를 추출
            sql= f'select password from users where email = \'{email}\''
						
			# 작성 해 놓은 쿼리문 실행
            cursor.execute(sql)
            
            # 레코드를 배열 형식으로 저장
            pwd = cursor.fetchall()
            
            # 그냥 출력 시 (('password'),) 튜플안에 튜플 형식으로 출력되어서
            # sprit으로 문자열 자르기(데이터 가공) : (('password'),) -> password
            # pwd = str(pwd)[3:-5]
            pwd = pwd[0][0]

			#비밀번호 체크
            if password == pwd:
		        #세션에 email을 user라는 키로 저장 구조 : {'user':email}
                request.session['user'] = email 
            else:
		        # 비밀번호가 틀렸을 때
                alert = {'msg':'이메일 또는 비밀번호가 잘못되었습니다.', 'url':'login2'}
        else:
		    #입력값이 없거나 계정을 잘 못 입력 했을 때
            alert = {'msg':'이메일 또는 비밀번호가 잘못되었습니다.', 'url':'login2'}
        # alert문이 공백이 아닐 경우(계정이 없거나 비밀번호가 틀렸을 시)
        # alert.html를 호출함과 동시에 메시지와 location 할 url값을 넘겨준다.
        if alert != "": return render(request, 'alert.html', {'msg' : alert})
        # 해당되는 url로 redirect
        return redirect(url)
    else:
		    #request 메소드가 get으로 오면 회원가입 페이지를 보여준다.
        return render(request, 'accounts/login2.html')
    
def login3(request):
		# 회원가입 성공 시 redirect 할 url 지정
    url = "polls:index"
    # 에러 유무를 구분하기 위한 변수
    alert = ""
    # request 메소드가 post로 오는지 확인, get이면 else문 실행
    if request.method == 'POST':
		    # email, password1로 전송된 값을 변수에 담아준다.
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email is not None and password is not None:
            # RowQuery를 Extue할 cursor 등록
            cursor = connection.cursor()
            
            # 쿼리문 작성 -> email이 일치하는 레코드의 Password를 추출
            sql = f'select email from users where email = \'{email}\' and password = \'{password}\''
						
			# 작성 해 놓은 쿼리문 실행
            cursor.execute(sql)
            
            # 레코드를 배열 형식으로 저장
            user = cursor.fetchall()
            
            # 데이터를 가공하기 전, 추출된 값이 있는지 확인, 값이 없다면 : 0
            if len(user) == 0:
                # 계정이 존재하지 않음
                alert = {'msg':'이메일 또는 비밀번호가 잘못되었습니다.', 'url':'login3'}
            else:
                #데이터 가공 user[0] -> (('data'),)
                #           user[0][0] -> data
                user = user[0][0]

                #세션에 user를 user라는 키로 저장 구조 : {'user':user}
                request.session['user'] = user
        else:
            #입력값이 없거나 계정을 잘 못 입력 했을 때
            alert = {'msg':'이메일 또는 비밀번호가 잘못되었습니다.', 'url':'login3'}
        # alert문이 공백이 아닐 경우(계정이 없거나 비밀번호가 틀렸을 시)
        # alert.html를 호출함과 동시에 메시지와 location 할 url값을 넘겨준다.
        if alert != "": return render(request, 'alert.html', {'msg' : alert})
        # 해당되는 url로 redirect
        return redirect(url)
    else:
		    #request 메소드가 get으로 오면 회원가입 페이지를 보여준다.
        return render(request, 'accounts/login3.html')
    
def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    print(request.session.keys())
    return redirect('polls:index')