"""signup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('testpage/', views.testpage, name="testpage"),
    path('loginpage/', views.loginpage, name="loginpage"),
    path('contactus/', views.contactus_page, name="contactus_page"),
    path('loginpage/signup/', views.handlesignup, name="signup"),
    path('loginpage/login/', views.handlelogin, name="login"),
    path('forgotpassword/', views.forgotpass_page, name="forgotpassword"),
    path('Handleforgotpass/', views.Handleforgotpass, name="Handleforgotpass"),
    path('changepassword/', views.changepass_page, name="changepass_page"),
    path('Handlechangepass/', views.Handlechangepass, name="Handlechangepass"),
    path('dashboard_password/', views.dashboard_password, name="changepass"),
    path('dashboard_change_password/', views.dashboard_password_authenticate, name="changepass"),
    path('logout/', views.handlelogout, name="logout"),
    path('redirect_loginpage/', views.redirect_loginpage, name="loginpage"),
    path('register/', views.register, name="register"),
    path('deregister_page/', views.deregister_page, name="deregister_page"),
    path('deregister/', views.deregister, name="deregister"),
    path('createevent/', views.createevent_page, name="createevent_page"),
    path('add_event/', views.addevent, name="addevent"),
    path('deleteevent/', views.deleteevent_page, name="deleteevent_page"),
    path('delete_event/', views.deleteevent, name="deleteevent"),
    path('modifyevent/', views.modifyevent_page, name="modifyevent_page"),
    path('modify_event_page/', views.modifyevent, name="modifyevent"),
    path('modify_event_handle/', views.modifyevent_handle, name="modifyevent_handle"),
    path('userprofile/', views.userprofile, name="userprofile"),
    path('update_details/', views.updatedetails, name="updatedetails"),
    path('404/', views.page404, name="page404"),
]
