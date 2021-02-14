from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import datetime


# Create your views here.

def home(request):
    return render(request,'home.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']


        if User.objects.filter(username=username).exists():
            messages.info(request, 'username already exists please login')
            return redirect('home')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'email already exists please login')
            return redirect('home')

        else:
            if password1 == password2:
                user = User.objects.create_user(
                    username=username, password=password1, email=email,first_name=fname,last_name=lname)
                user.save()
                messages.info(request, 'account created for' +' '+username)
                return redirect('register')
            else:
                messages.info(request, 'password not matching')
                return redirect('register')
    else:
        return render(request,'register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
            return redirect("login")
    else:
        return render(request,'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')

def dashboard(request,emp_id):
    x = datetime.datetime.now()
    date=x.strftime("%d")+'/'+x.strftime("%b")+'/'+x.strftime("%Y")
    time=x.strftime("%I")+':'+x.strftime("%M")+' '+x.strftime("%p")

    employee=User.objects.get(id=emp_id)
    attandance=Attendance.objects.filter(emp=employee,date=date)
    status=attandance.count()

    if(status==1):
        task = Attendance.objects.get(emp=employee,date=date).task
    else:
        task=''

    preMonthSalary=0
    preMonth=''
    year=''
    if(x.strftime("%b")=='Jan'):
        year=str(x.year-1)
        preMonth='Dec'
        attandance=Attendance.objects.filter(emp=employee)
        count=0

        if attandance.count() !=0:
            for i in attandance:
                if(preMonth+'/'+year in i.date):
                    count+=1
                else:
                    continue

        preMonthAttandance=count
        preMonthSalary=int(employee.employee.perDaySalary)*preMonthAttandance

    else:
        year=str(x.strftime("%Y"))
        month=int(x.month)
        preMonth="Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(' ')[month-2]
        attandance=Attendance.objects.filter(emp=employee)
        count=0
        if attandance.count() !=0:
            for i in attandance:
                if(preMonth+'/'+year in i.date):
                    count+=1
                else:
                    continue

        preMonthAttandance=count
        preMonthSalary=int(employee.employee.perDaySalary)*preMonthAttandance

        
    notices=Notice.objects.all().order_by('-date')
    active=notices[0].id

    
    preMonthBonus=employee.employee.bonus
    context={'date':date,'time':time,'status':status,'task':task,'preMonth':preMonth,'year':year,'preMonthSalary':preMonthSalary,'preMonthBonus':preMonthBonus,'notices':notices}
    return render(request,'dashboard.html',context)

def attandance(request,emp_id):
    officeTime=[9,0,'AM']
    timeNow=datetime.datetime.now()
    minute=int(timeNow.strftime("%M"))
    hour=int(timeNow.strftime("%I"))
    p=timeNow.strftime("%p")
    delay=minute-officeTime[1]
    print(delay)
    employee=User.objects.get(id=emp_id)
    date=timeNow.strftime("%d")+'/'+timeNow.strftime("%b")+'/'+timeNow.strftime("%Y")

    if delay<20 and hour==9 and p=='AM':
        markAttend=Attendance(emp=employee,status=True,date=date)
        markAttend.save()
        messages.info(request,'Your attandance is marked successfully')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request,'Attandance Window is closed be punctual from next time')
        return redirect(request.META.get('HTTP_REFERER'))

        
def update(request,emp_id):
    if request.method=='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        addr = request.POST['address']
        phone = request.POST['phone']
        password=request.POST['password']
        pic = request.FILES.get('pic', False)
        emp=User.objects.get(id=emp_id)

        if fname!='':
            emp.first_name=fname
            emp.save()
            messages.info(request,'First Name updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        elif lname!='':
            emp.last_name=lname
            emp.save()
            messages.info(request,'Last Name updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        elif email!='':
            emp.email=email
            emp.save()
            messages.info(request,'Email updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        elif phone!='':
            emp.employee.phone=phone
            emp.employee.save()
            messages.info(request,'Phone updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        elif addr!='':
            emp.employee.address=addr
            emp.employee.save()
            messages.info(request,'Address updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        elif password!='':
            emp.set_password(password)
            emp.save()
            messages.info(request,'Password updated successfully')
            return redirect('login')
        elif pic!=False:
            emp.employee.img=pic
            emp.employee.save()
            messages.info(request,'Profile Picture updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(request.META.get('HTTP_REFERER'))

    else:
        return render(request,'update.html')