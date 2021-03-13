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

    #day month year
    day=int(x.strftime("%d"))
    month=x.strftime("%b")
    year=int(x.strftime("%Y"))

    date=x.strftime("%d")+'/'+x.strftime("%b")+'/'+x.strftime("%Y")

    time=x.strftime("%I")+':'+x.strftime("%M")+' '+x.strftime("%p")

    employee=User.objects.get(id=emp_id)
    attandance=Attendance.objects.filter(emp=employee,day=day,month=month,year=year)
    status=attandance.count()

    if(status==1):
        task = Attendance.objects.get(emp=employee,day=day,month=month,year=year).task
    else:
        task=''


    if(x.strftime("%b")=='Jan'):
        year=int(x.year-1)
        preMonth='Dec'
        attandance=Attendance.objects.filter(emp=employee,month=preMonth,year=year)

        preMonthAttandance=attandance.count()
        preMonthSalary=int(employee.employee.perDaySalary)*preMonthAttandance

    else:
        year=int(x.strftime("%Y"))
        month=int(x.month)
        preMonth="Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(' ')[month-2]
        attandance=Attendance.objects.filter(emp=employee,month=preMonth,year=year)
        preMonthAttandance=attandance.count()
        preMonthSalary=int(employee.employee.perDaySalary)*preMonthAttandance

        
    notices=Notice.objects.all().order_by('-date')
    active=notices[0].id

    
    preMonthBonus=employee.employee.bonus
    context={'date':date,'time':time,'status':status,'task':task,'preMonth':preMonth,'year':year,'preMonthSalary':preMonthSalary,'preMonthBonus':preMonthBonus,'notices':notices}
    return render(request,'dashboard.html',context)

def attandance(request,emp_id):
    officeTime=[9,0,'AM']
    x=datetime.datetime.now()
    minute=int(x.strftime("%M"))
    hour=int(x.strftime("%I"))
    p=x.strftime("%p")
    delay=minute-officeTime[1]

    employee=User.objects.get(id=emp_id)

    day=int(x.strftime("%d"))
    month=x.strftime("%b")
    year=int(x.strftime("%Y"))

    if delay<20 and hour==officeTime[0] and p==officeTime[2]:
        markAttend=Attendance(emp=employee,status=True,day=day,month=month,year=year)
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

        if lname!='':
            emp.last_name=lname
            emp.save()
            messages.info(request,'Last Name updated successfully')

        if email!='':
            emp.email=email
            emp.save()
            messages.info(request,'Email updated successfully')
            
        if phone!='':
            emp.employee.phone=phone
            emp.employee.save()
            messages.info(request,'Phone updated successfully')
            
        if addr!='':
            emp.employee.address=addr
            emp.employee.save()
            messages.info(request,'Address updated successfully')
            
        if password!='':
            emp.set_password(password)
            emp.save()
            messages.info(request,'Password updated successfully')
            
        if pic!=False:
            emp.employee.img=pic
            emp.employee.save()
            messages.info(request,'Profile Picture updated successfully')
           
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        return render(request,'update.html')