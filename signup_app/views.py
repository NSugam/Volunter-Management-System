from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .helper import generateOTP
from .models import Event_table, Registration

def page404(request):
    return render(request,"404.html")

def index(request):
    username = request.user.username
    event = Event_table.objects.all()
    registered = Registration.objects.filter(username = username)
    params = {'event': event, 'registrations':registered}
    return render (request,"index.html", params)

def redirect_loginpage(request):
    messages.error(request, 'Login First to Register')
    return redirect(loginpage)

def createevent_page(request):
    return render (request,"handle_event/createevent.html")

def deleteevent_page(request):
    return render (request,"handle_event/deleteevent.html")

def deregister(request):
    if request.method == 'POST':
        event_name = request.POST['event_name']

        registration_table_data = Registration.objects.all()
        for i in registration_table_data:
            if i.username == request.user.username:
                if i.event_name == event_name:
                    delete_event_01 = Registration.objects.filter(event_name = i.event_name)
                    delete_event = delete_event_01.get(username = i.username)
                    delete_event.delete()
                    messages.success(request, 'Sorry to hear that you have de-registered from an event')
                    return redirect(index)

    return render (request,"handle_event/deregister.html")

def addevent(request):
    if request.method == 'POST':
        event_name = request.POST['event_name']
        description = request.POST['description']
        event_price = request.POST['event_price'] 
        new_event = Event_table()
        new_event.event_name = event_name
        new_event.description = description
        new_event.event_price = event_price
        new_event.save()
        messages.success(request, 'Event has been registered')
        return redirect(index)
    else:
        return render(page404)

def deleteevent(request):
    if request.method == 'POST':
        event_name = request.POST['event_name']

        if not Event_table.objects.filter(event_name = event_name):
            messages.success(request, "Event Name doesn't exist")
            return redirect(deleteevent_page)

        delete_event = Event_table.objects.get(event_name=event_name)
        delete_event.delete()
        messages.success(request, 'Event has been deleted')
        return redirect(index)
    else:
        return render(page404)

def register (request):
    if request.method == 'POST':
        event_name = request.POST['event_name']
        event_table_data = Event_table.objects.all()
        for i in event_table_data:
            if i.event_name == event_name:
                event_price = i.event_price

        registration_table_data = Registration.objects.all()
        for i in registration_table_data:
            if i.username == request.user.username and i.event_name == event_name:
                messages.success(request, 'You cannot register twice')
                return redirect(index)

        register_event = Registration()
        register_event.username = request.user.username
        register_event.firstname = request.user.first_name
        register_event.event_name = event_name
        register_event.event_price = event_price
        register_event.save()

        messages.success(request, 'Event has been registered')
        
        params = {'event_name':event_name, 'event_price':event_price}
        return render (request,"handle_event/register.html", params)

    else:
        return redirect(page404)

def loginpage(request):
    return render (request,"login_signup/loginpage.html")

def contactus_page(request):
    return render (request,"contactus.html")

def forgotpass_page(request):
    return render (request,"login_signup/forgotpassword.html")

def dashboard_password(request):
    return render (request,"dashboard_password.html")

def changepass_page(request):
    try:
        get_username = request.session['username']
        token = request.session['token']
        return render (request,"changepassword.html")
    except:
        return redirect(page404)

def Handlechangepass(request):
    try:
        get_username = request.session['username']
        token = request.session['token']

        get_token = request.POST['get_token']
        new_password = request.POST['new_pswd']
        new_password2 = request.POST['new_pswd2']

        if token == get_token:
            if new_password == new_password2:
                change_pswd = User.objects.get(username= get_username)
                change_pswd.set_password(new_password)
                change_pswd.save()
                messages.success(request, 'Password Changed ! You can now login')
                del request.session['token']
                return redirect(loginpage)
            else:
                messages.error(request, 'Password Not Matched')
                return redirect(changepass_page)
        else:
            messages.error(request, 'OTP Incorrect')
            return redirect(changepass_page)
    except:
        return redirect(page404)

def Handleforgotpass(request):
    if request.method == 'POST':
        username = request.POST['forgot_uname']

        if not User.objects.filter(username = username).first():
            messages.error(request, 'Email address does not exist')
            return redirect(forgotpass_page)

        request.session['username'] = username
        token = generateOTP(username)
        request.session['token'] = token

        
        messages.success(request, 'OTP sent to your email')

        return redirect (changepass_page)

    else:
        return redirect(page404)

def handlesignup (request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['pswd']
        cpassword = request.POST['cpswd']
        username = email

        if User.objects.filter(email = email).first():
            messages.error(request, 'Email address already exist')
            return redirect(loginpage)

        if password != cpassword:
            messages.error(request, 'Password Not Matched')
            return redirect(loginpage)
        
        createuser = User.objects.create_user(username,email,password)
        createuser.first_name = firstname
        createuser.last_name = lastname
        createuser.save()
        messages.success(request,"Account Created Successfully")
        return redirect(loginpage)

    else:
        return redirect(page404)

def handlelogin(request):
    if request.method == 'POST':
        login_username = request.POST['login_uname']
        login_password = request.POST['login_pswd']

        user = authenticate(username= login_username, password= login_password)

        if user is not None:
            login(request, user)
            messages.success(request,f"Welcome {request.user.first_name}, Account Login Successfull")
            return redirect (index)
        else:
            messages.error(request, 'Invalid Email Address or Password')
            return redirect (loginpage)

    else:
        return HttpResponse('404 - Forbidden')

def handlelogout(request):
    messages.success(request, f"Bye Bye {request.user.first_name}, See you soon")
    logout(request)
    return redirect (index)