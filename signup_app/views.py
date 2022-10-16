from turtle import home
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .helper import generateOTP
from .models import Event_table, Registration
from datetime import datetime,timedelta

def testpage(request):
    if request.user.is_authenticated:
        messages.success(request, 'Thank you for your enquiry ! We will contact you as soon as possible.')
        return redirect(index)
        # return HttpResponse ("Got it")
    else:
        return redirect(redirect_loginpage)


def page404(request):
    return render(request,"404.html")

def index(request):
    global event_table_data, past_events, ongoing_events, upcoming_events, registered
    username = request.user.username
    event_table_data = Event_table.objects.all()
    registered = Registration.objects.filter(username = username)
    CurrentDate = datetime.now()
    YestardayDate = datetime.now()-timedelta(1)
    TomorrowDate = datetime.now()+timedelta(1)
    past_events = Event_table.objects.filter(event_date__range = ["2020-01-01",YestardayDate])
    ongoing_events = Event_table.objects.filter(event_date = CurrentDate)
    upcoming_events = Event_table.objects.filter(event_date__range = [TomorrowDate,"2030-01-01"])
    params = {
        'event': event_table_data, 
        'registrations': registered, 
        'past_events': past_events,
        'ongoing_events': ongoing_events,
        'upcoming_events': upcoming_events,
        'CurrentDate': CurrentDate
    }
    return render (request,"index.html", params)

def redirect_loginpage(request):
    messages.error(request, 'Login First to Continue')
    return redirect(loginpage)

def createevent_page(request):
    if request.user.is_superuser:
        return render (request,"handle_event/createevent.html")
    else:
        return redirect(page404)

def deleteevent_page(request):
    if request.user.is_superuser:
        params = {'event': event_table_data}
        return render (request,"handle_event/deleteevent.html", params)
    else:
        return redirect(page404)

def modifyevent_page(request):
    if request.user.is_superuser:
        params = {'event': event_table_data}
        return render (request,"handle_event/modifyevent.html", params)
    else:
        return redirect(page404)

def modifyevent(request):
    if request.method == 'POST':
        event_name = request.POST['event_name']
        event_name_filter = Event_table.objects.filter(event_name = event_name)
        params = {'event_name_filter':event_name_filter}
        return render (request,"handle_event/modifyevent1.html", params)

def modifyevent_handle(request):
    if request.user.is_authenticated:
        event_name = request.POST['event_name']
        event_price = request.POST['event_price']
        event_date = request.POST['event_date']
        try:
            formatDate = datetime.strptime(event_date,"%b. %d, %Y")
        except:
            try:
                formatDate = datetime.strptime(event_date,"%B %d, %Y")
            except:
                try:
                    formatDate = datetime.strptime(event_date,"%Y-%m-%d")
                except:
                    messages.success(request, 'Date Format is Incorrect (YYYY-MM-DD IS REQUIRED)')
                    return redirect (modifyevent_page)
       
            update_event = Event_table.objects.get(event_name = event_name)
            update_event.event_name = event_name
            update_event.event_price = event_price
            update_event.event_date = formatDate
            update_event.save()
            messages.success(request, f'{event_name} Event has been modified')
            return redirect(index)
        



def deregister_page(request):
    if request.user.is_authenticated:
        params = {'registrations': registered}
        return render (request,"handle_event/deregister.html",params)
    else:
        return redirect(page404)

def deregister(request):
    try:
        if request.method == 'POST':
            event_name = request.POST['event_name']
            username = request.user.username
            delete_event_01 = Registration.objects.filter(username = username)
            delete_event = delete_event_01.get(event_name = event_name)
            delete_event.delete()
            messages.success(request, 'Sorry to hear that you have de-registered from an event')
            return redirect(index)
        else:
            return redirect(page404)
    except:
        messages.success(request, 'You have not registered')
        return redirect(deregister_page)


def addevent(request):
    try:
        if request.method == 'POST':
            event_name = request.POST['event_name']
            description = request.POST['description']
            event_price = request.POST['event_price'] 
            event_date = request.POST['event_date']
            new_event = Event_table()
            new_event.event_name = event_name
            new_event.description = description
            new_event.event_price = event_price
            new_event.event_date = event_date
            new_event.save()
            messages.success(request, 'Event has been registered')
            return redirect(index)
        else:
            return render(page404)
    except:
            messages.success(request, 'Date Format is Incorrect')
            return redirect(createevent_page)

def deleteevent(request):
    if request.method == 'POST':
        event_name = request.POST['event_name']

        if not Event_table.objects.filter(event_name = event_name):
            messages.success(request, "Event Name doesn't exist")
            return redirect(deleteevent_page)

        delete_event = Event_table.objects.get(event_name=event_name)
        delete_event.delete()
        messages.success(request, f'{event_name} Event has been deleted')
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
                event_date = i.event_date

        registration_table_data = Registration.objects.all()
        for i in registration_table_data:
            if i.username == request.user.username and i.event_name == event_name:
                messages.success(request, 'You cannot register twice')
                return redirect(index)

        register_event = Registration()
        register_event.username = request.user.username
        register_event.firstname = request.user.first_name
        register_event.event_name = event_name
        register_event.save()

        messages.success(request, 'Event has been registered')
        
        params = {'event_name':event_name, 'event_price':event_price}
        return render (request,"handle_event/register.html", params)

    else:
        return redirect(page404)

def loginpage(request):
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged In')
        return redirect(index)
    else:
        return render (request,"login_signup/loginpage.html")
        
def contactus_page(request):
    return render (request,"contactus.html")

def forgotpass_page(request):
    return render (request,"login_signup/forgotpassword.html")

def dashboard_password(request):
    if request.user.is_authenticated: 
        return render (request,"dashboard_password.html")
    else:
        return redirect(page404)

def userprofile(request):
    if request.user.is_authenticated: 
        return render (request,"userprofile.html")
    else:
        return redirect(loginpage)

def updatedetails (request):
    if request.user.is_authenticated:
        username = request.POST['username']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        update_user = User.objects.get(username= username)
        update_user.username = username
        update_user.email = username
        update_user.first_name = firstname
        update_user.last_name = lastname
        update_user.save()
        messages.success(request, 'Account Details Changed')
        return redirect(index)

def dashboard_password_authenticate(request):
    if request.method == 'POST':
        username = request.user.username
        old_password = request.POST['old_pass']
        new_password = request.POST['new_pass']
        new_password2 = request.POST['new_pass2']
        user = authenticate(username= username, password= old_password)
        if user is not None and new_password == new_password2:
            change_pswd = User.objects.get(username= username)
            change_pswd.set_password(new_password)
            change_pswd.save()
            messages.success(request, 'Password Changed. Please Login Again')
            return redirect(index)
        else:
            messages.success(request, 'Old password is Incorrect')
            return redirect(dashboard_password)
    else:
        return redirect(page404)

def changepass_page(request):
    try:
        token = request.session['token']
        return render (request,"login_signup/changepassword.html")
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
                logout(request)
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
        print(token)
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
        return redirect(page404)

def handlelogout(request):
    messages.success(request, f"Bye Bye {request.user.first_name}, See you soon")
    logout(request)
    return redirect (index)