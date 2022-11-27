from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.login,name='login'),
    path('',views.home, name='home'),
    path('bill/',views.bill, name="menu"),
    path('bill/final/',views.final, name="final"),
    path('register/',views.register, name="register"),
    path('user/',views.user, name="user"),
    path('employee/',views.employee, name="employee"),
    path('adddetails/',views.adddetails, name="adddetails"),
    path('adddetails/additems/',views.additems, name="additems"),
    path('adddetails/removeitems/',views.removeorders, name="removeorders"),
    path('adddetails/makepayments/',views.makepayments, name="makepayments"),
]