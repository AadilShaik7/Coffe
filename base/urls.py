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
]