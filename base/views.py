from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def home(request):
    if request.method=='POST':
        x=str(request.body)
        x=x[2:len(x)-1]
        x=x.split("&")
        for i in x:
            
            with connection.cursor() as cursor:
                cursor.execute("select * from login")
                columns = [column[0] for column in cursor.description]
                data = []
                for row in cursor.fetchall():
                    data.append(dict(zip(columns, row)))
                y=int(data[0]['id'])
                cursor.execute("select * from menu where Item_id = (%s)",
                [i[0]],
                )
                columns = [column[0] for column in cursor.description]
                data = []
                for row in cursor.fetchall():
                    data.append(dict(zip(columns, row)))
                    p=(int(i[2]))*(int(row[2]))
                    cursor.callproc('updatecart',[i[0],y,i[2],p])
        return render(request,'home.html',{'dic':data})

    else:    
        with connection.cursor() as cursor:
            cursor.execute("select * from menu")
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))
        return render(request,'home.html',{'dic':data})


@csrf_exempt
def bill(request):
    if request.method=='POST':
        x=str(request.body)
        x=x[2:len(x)-1]
        data=[]
        with connection.cursor() as cursor:
            cursor.execute("select * from login")
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))
            y=int(data[0]['id'])
        if x== "payment":
            with connection.cursor() as cursor:
                cursor.callproc('payment',[y])
                cursor.execute("select * from customer_order where CustomerID=%s",
                [y])
                columns = [column[0] for column in cursor.description] 
                for row in cursor.fetchall():
                    data.append(dict(zip(columns, row)))
            return render(request,'final.html',{'dic':data})
        else:
            x=int(x)
            with connection.cursor() as cursor:
                cursor.execute("Delete from cart where Customer_id=%s and Item_id=%s",[y,x])
                cursor.execute("select * from cart")
                columns = [column[0] for column in cursor.description]
                data = []
                i=0
                for row in cursor.fetchall():
                    data.append(dict(zip(columns, row)))
                s=0
                for i in range(0,len(data)):
                    s=s+data[i]["price"]
                    cursor.execute("select Item_Name from menu where Item_id = (%s)",
                        [data[i]['Item_id']])
                    for j in cursor:
                        data[i]["Name"]=j[0]
                    for i in range(0,len(data)):
                        data[i]["Total"]=s
            return render(request,'bill.html',{'dic':data})

    else:
        with connection.cursor() as cursor:
            cursor.execute("select * from cart")
            columns = [column[0] for column in cursor.description]
            data = []
            i=0
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))
            s=0
            for i in range(0,len(data)):
                s=s+data[i]["price"]
                cursor.execute("select Item_Name from menu where Item_id = (%s)",
                    [data[i]['Item_id']])
                for j in cursor:
                    data[i]["Name"]=j[0]
                for i in range(0,len(data)):
                    data[i]["Total"]=s
            
        return render(request,'bill.html',{'dic':data})

@csrf_exempt
def final(request):
    if request.method=="POST":
        with connection.cursor() as cursor:
            cursor.execute("select * from login")
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))
            y=int(data[0]['id'])
            print(y)
            cursor.execute("select * from customer_order where CustomerID=%s",[y])
            columns = [column[0] for column in cursor.description]
            data = []   
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))
            cursor.execute("delete from login where id=%s",[y])
        return render(request,'final.html',{'dic':data})
    else:
        with connection.cursor() as cursor:
            cursor.execute("select * from login")
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))
            y=int(data[0]['id'])
            print(y)
            cursor.execute("select * from customer_order where CustomerID=%s",[y])
            columns = [column[0] for column in cursor.description]
            data = []   
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))
        return render(request,'final.html',{'dic':data})


@csrf_exempt
def login(request):
    return render(request,'login.html')

@csrf_exempt
def register(request):
    if request.method=='POST':
        username=request.POST['Username']
        firstname=request.POST['Firstname']
        email=request.POST['Emailid']
        password=request.POST['password']
        with connection.cursor() as cursor:
            cursor.execute("Insert into customer(CustomerName,email,pwd,username) values(%s,%s,%s,%s)"
            ,[firstname,email,password,username])
        return render(request,'user.html')

    else:
        return render(request,'register.html')

@csrf_exempt
def user(request):
    response_data = {"is_success":False}
    if request.method=='POST':
        username=request.POST['Name']
        pwd=request.POST['Pwd']
        with connection.cursor() as cursor:
            cursor.execute("select * from customer where username=%s and pwd=%s",
            [username,pwd])
            c=0
            x=0
            
            for row in cursor.fetchall():
                x=x+1
                data=[]
                columns = [column[0] for column in cursor.description]
                data.append(dict(zip(columns, row)))
                y=int(data[0]['CustomerID'])
                if x==1:
                    response_data["is_success"]=True
                    cursor.execute("Insert into login values(%s,%s,%s)",
                    [username,pwd,y])
                c=row[0]
            cursor.execute("select * from menu")
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))
        return JsonResponse(response_data)
    else:
        return render(request,'user.html')

@csrf_exempt
def employee(request):
    response_data = {"is_success":False}
    if request.method=='POST':
        username=request.POST['Name']
        pwd=request.POST['Pwd']
        with connection.cursor() as cursor:
            cursor.execute("select * from employee where employee_name=%s and pwd=%s",
            [username,pwd])
            c=0
            x=0
            
            for row in cursor.fetchall():
                x=x+1
                if x==1:
                    response_data["is_success"]=True
                c=row[0]
        return JsonResponse(response_data)
    else:
        return render(request,'employee.html')

@csrf_exempt
def adddetails(request):
    return render(request,'adddetails.html')

@csrf_exempt
def additems(request):
    if request.method=="POST":
        itemname=request.POST["itemname"]
        Price=request.POST["price"]
        with connection.cursor() as cursor:
            cursor.execute("INSERT into menu(Item_Name,Price) values (%s,%s)",
            [itemname,Price])
        return render(request,'adddetails.html')
    else:    
        return render(request,'additems.html')

@csrf_exempt
def removeorders(request):
    if request.method=='POST':
        x=str(request.body)
        x=x[2:len(x)-1]
        data=[]
        x=int(x)
        with connection.cursor() as cursor:
            cursor.execute("select * from login")
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))
            cursor.execute("Delete from customer_order where order_id=%s",[x])
            data = []
            i=0
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))
            s=0
        return render(request,'adddetails.html')
    else:
        with connection.cursor() as cursor:
            cursor.execute("select * from customer_order")
            columns = [column[0] for column in cursor.description]
            data = []
            i=0
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))    
        return render(request,'Removeorders.html',{'dic':data})


@csrf_exempt
def makepayments(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from employeePayments")
        columns = [column[0] for column in cursor.description]
        data = []
        i=0
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))    
    return render(request,'makepayments.html',{'dic':data})
    