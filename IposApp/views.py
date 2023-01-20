from ast import Not, Num, Return, excepthandler, operator
from atexit import register
from base64 import encode
import base64
from distutils.log import error
from email.utils import encode_rfc2231
from locale import currency
import re
from tokenize import Special
from unicodedata import decimal
from django.core import serializers
import json
from calendar import monthcalendar
from ctypes import cast, sizeof
from ctypes.wintypes import CHAR
from dis import dis
from email import message
from email.encoders import encode_base64
from encodings import utf_8, utf_8_sig
import imp
from itertools import count
from json import JSONEncoder
from lib2to3.pytree import convert
from multiprocessing import context
import numbers
import os
from pickle import bytes_types
from pydoc import render_doc
from random import randrange
from re import X
from sqlite3 import Cursor, Date, Row
from ssl import AlertDescription
import string
from sys import maxsize
from telnetlib import ENCRYPT
import tempfile
from datetime import date, datetime
from this import s
from time import time


from urllib import response
from urllib.parse import urlencode
from urllib.request import Request
from xmlrpc.client import DateTime


from django.conf import settings
from django.db.backends import mysql
from django.shortcuts import render
import pyodbc
from django.contrib import messages
from django.contrib.sites import requests
from django.db import connections
from django.http import HttpResponse, HttpResponseBadRequest, Http404,HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime as dt



from django.template.loader import get_template
# from easy_pdf.rendering import render_to_pdf_response
# from xhtml2pdf import pisa
from fpdf import FPDF, fpdf
# import PyPDF2
# from easy_pdf.views import PDFTemplateView

# import reportlab
import io
from django.http import FileResponse
from django.contrib.auth.hashers import make_password
from django.contrib import auth

from django.db import connection
from django.contrib import sessions

import urllib
# from reportlab.pdfgen import canvas
from django.http import JsonResponse

import pandas as pd



conn = pyodbc.connect(
    'Driver={SQL Server Native Client 10.0};'
    f'Server=SUMMIT-6\SQLEXPRESS;'
    f'Database=IPOS_PromoTest;'
    f'UID=sa;'
    f'PWD=123;'
    'Mars_Connection=Yes;'
)
def Reg(request):
    if 'EmployeeName' not in request.session:
        return render(request,'EmpRegistration.html')
    s='pending'
    if request.method == "POST":
        CustomerName=request.POST['CustomerName']
        MobileNumber = request.POST['MobileNumber']
        NoOfPerson = request.POST['NoOfPerson']
        SelectTable = request.POST['SelectTable']
        TokenTime = request.POST['TokenTime']
        cursor = conn.cursor()
        TokenTime = datetime.now()
        query = "INSERT INTO Register(CustomerName,MobileNumber,NoOfPerson,SelectTable,TokenTime,Status) VALUES(?,?,?,?,?,?)"
        cursor.execute(query, (CustomerName, MobileNumber, NoOfPerson,SelectTable,TokenTime,s))
        conn.commit()
        # messages.success(request,'Successfully Registered...')
        

        cursor = conn.cursor()
        user = "SELECT * FROM Register WHERE id = (SELECT MAX(Id)FROM Register);"
        cursor.execute(user)
        user = cursor.fetchall()
        cursor.commit()
        pdf = FPDF('P', 'mm', 'A5')
        pdf.add_page()
        pdf.set_font('Times', '',size=25)
        pdf.cell(40, 10, "Arakkal Palace", 0, 1)
        pdf.line(1, 20, 85, 20)
        pdf.line(1, 70, 85, 70)
        pdf.cell(40, 10, '', 0, 1)
        pdf.set_font('Times', '', 10)

       
        for line in user:
            pdf.cell(20, 8, 'CustomerName :    ' + line.CustomerName, 0, 1, '\t')
            pdf.cell(20, 8, 'MobileNumber :    ' + line.MobileNumber, 0, 1)
            pdf.cell(20, 8, 'NoOfPerson   :      ' + str(line.NoOfPerson), 0, 1)
            pdf.cell(20, 8, 'Table        :           ' + line.SelectTable, 0, 1)
            pdf.cell(20, 8, 'TokenTime    :       ' + str(line.TokenTime), 0, 1)
            pdf.cell(20, 8, 'TokenNumber  :         ' + str(line.id), 0, 1)

        filename = tempfile.mktemp('.pdf')
        open(filename, "w").readable()
        pdf.output('report.pdf', 'F')
        messages.success(request,"Sucessfully Registred....")
        # return FileResponse(open('report.pdf', 'rb'))
        return redirect('/Display')
    tb = conn.execute("select * from R_Table")
    return render(request, 'Registration.html',{'tb':tb})
    


def report(request,id):
    global k
    cursor=conn.cursor()
    user="SELECT * FROM Register WHERE id ="+str(id)
    cursor.execute(user)
    user=cursor.fetchall()
    num = request.GET.dict()
    print(num)
    num = request.GET.dict()
    print(num)
    for k in num.values():
        print("ans:",k)
    cursor = conn.cursor()
    cursor.execute("UPDATE Register SET SelectTable = ? WHERE id ="+str(id),k)
    cursor.commit()
    
    
    
    pdf = FPDF('P', 'mm', 'A5')
    pdf.add_page()
    pdf.set_font('Times', 'B', 18,)
    pdf.rect(1, 20, 95, 110)

    pdf.cell(40, 40,"Arakkal Palace", 0, 1,)
    pdf.image('static/images/Arakkal1.jpg',15,35,30,20,'JPG','')
    pdf.line(1, 60, 96, 60)
    # pdf.cell(40, 10, '', 0, 1)
    pdf.set_font('Times', 'B', 12)
    
   
    for line in user:
        
        pdf.cell(20, 10,'    ' , 0, 1)
        pdf.cell(20, 10,'CustomerName :    ' + line.CustomerName, 0, 1,'\t')
        pdf.cell(20, 10,'MobileNumber :    ' + line.MobileNumber, 0, 1)
        pdf.cell(20, 10,'NoOfPerson   :      ' + str(line.NoOfPerson), 0, 1)
        pdf.cell(20, 10,'Table        :           ' + line.SelectTable, 0, 1)
        pdf.cell(20, 10,'TokenTime    :       ' + str(line.TokenTime), 0, 1)
        pdf.cell(20, 10,'TokenNumber      :         ' + str(line.id), 0, 1)

    filename = tempfile.mktemp('.jpg')
    open(filename, "w").readable()
    pdf.output('report.pdf', 'F') 
    return FileResponse(open('report.pdf', 'rb'))
    
   
  
def Display(request):
    if 'EmployeeName' not in request.session:
        return render(request,'EmpRegistration.html')
    if request.session.has_key:
        user=request.session['EmployeeName']
        cursor = conn.cursor()
        cursor.execute("select * from Register where Status='pending' order by id ASC")
        result = cursor.fetchall()
        cursor.execute("select TableNo from R_Table")
        tb=cursor.fetchall()
    return render(request, 'index.html', {'result': result,'tb':tb,'user':user})
    


k=''
def update(request, id):
     if request.session.has_key:
        global k
        a = 'Approved'
        key = request.POST.getlist("arr[]")
        num = request.GET.dict()
        print(num)
        for k in num.values():
            print("ans:", k)
        cursor = conn.cursor()
        time = "'" + str(datetime.now()) + "'"
        # res="UPDATE Register SET TokenIn=CONVERT(DATETIME,getdate()) WHERE id = "+str(id)
        cursor.execute("UPDATE Register SET TokenIn=CONVERT(DATETIME,getdate()),SelectTable = ?,Status=? WHERE id =" + str(id), k,a)
        cursor.commit()
        return redirect('/Display')
    
    

k=''
def updt(request,id):
    global k
    a = 'Approved'
    key = request.POST.getlist("arr[]")
    num = request.GET.dict()
    print(num)
    for k in num.values():
        print("ans:",k)
    cursor = conn.cursor()
    cursor.execute("UPDATE Register SET Status=?,SelectTable = ?  WHERE id = ?",a,k,id)
    cursor.commit()
    return redirect('/Display')


def show(request,id):
    if 'EmployeeName' not in request.session:
        return render(request,'EmpRegistration.html')
    cursor=conn.cursor()
    user=("Select * from Register where id="+str(id))
    cursor.execute(user)
    user=cursor.fetchone()
    tb = conn.execute("select TableNo from R_Table")
    return render(request,'Edit.html',{'user':user,'tb':tb})



m='Cancel'
def Stat(request,id):
    cursor=conn.cursor()
    cursor.execute("UPDATE Register SET Status = ? WHERE id = ?",m,id)
    conn.commit()
    # st=cursor.fetchall()
    return redirect('/Display')


def Home(request):
    if 'EmployeeName' not in request.session:
        return render(request,'EmpRegistration.html')
    if request.session.has_key:
        user=request.session['EmployeeName']
        return render(request,'index4.html',{'user':user})

def FinalReports(request):
    if 'EmployeeName' not in request.session:
        return render(request,'EmpRegistration.html')
    if request.session.has_key:
        user=request.session['EmployeeName']
        cursor=conn.cursor()
        cursor.execute("select * from Register order by TokenIn DESC ")
        user=cursor.fetchall()
        conn.commit()
    return render(request,'FinalReports.html',{'user':user})



def Tables(request):
    if 'EmployeeName' not in request.session:
        return render(request,'EmpRegistration.html')
    if request.session.has_key('EmployeeName'):
        cursor=conn.cursor()
        cursor.execute("Select tableNo from R_Table")
        res=cursor.fetchall()
        cursor.execute("SELECT rtrim(R_Table.TableNo) as tableNo,BkColor,R_Table.Available,Sum(Case when KOT_Status Not in ('Closed','Void') then GrandTotal else NULL end) as Amt, Max(Case when KOT_Status Not in ('Closed','Void') then Convert(nvarchar(20),DateDiff(Minute,(BillDate),GetDate()))+' Min' else NULL end) as Tm,max(Case when KOT_Status Not in ('Closed','Void') then id else NULL end) as id,R_table.NoOfChairs as totChairs, Sum(Case when KOT_Status Not in ('Closed','Void') then RestaurantPOS_OrderInfoKOT.NoOfPax else 0 end) as NoOfChairsbooked,Count(RestaurantPOS_OrderInfoKOT.ID) as NoOfBill, R_table.NoOfChairs - Sum(Case when KOT_Status Not in ('Closed','Void') then RestaurantPOS_OrderInfoKOT.NoOfPax else 0 end) as vacantchair From R_Table left Join RestaurantPOS_OrderInfoKOT On R_Table.TableNo=Left(RestaurantPOS_OrderInfoKOT.TableNo, Len(RTrim(RestaurantPOS_OrderInfoKOT.TableNo)) - 3) And RestaurantPOS_OrderInfoKOT.KOT_Status = 'open'Where R_Table.branchid = 1 And Status ='Activate'group By R_Table.TableNo,BkColor,Available,R_table.NoOfChairs,RestaurantPOS_OrderInfoKOT.TableNo ORDER BY  Left(R_Table.TableNo, PATINDEX('%[0-9]%', R_Table.TableNo)-1),Convert(Int, SUBSTRING(R_Table.TableNo, PATINDEX('%[0-9]%',R_Table.TableNo), Len(R_Table.TableNo)))")
        result=cursor.fetchall()  
        global count
        for x in res:
            if count!=x:
                continue        
        count=x
    return render(request,'Table.html',{'user':result,'res':res,'count':count})


def log(request):
    if request.method=="POST":
        EmployeeName=request.POST["EmployeeName"]
        Password=request.POST["Password"]
        sample_string_bytes = Password.encode("utf-8")

        base64_bytes = base64.b64encode(sample_string_bytes)
        ENpassword = base64_bytes.decode("utf-8")

        ## new_key = base64.b64encode(bytes(str(Password), encoding='utf-8'))
       
        cursor=conn.cursor()
        sql="Select EmployeeName,EmpId  from  EmployeeRegistration WHERE  EmployeeName ='"+EmployeeName+"'  AND  Password ='"+ENpassword+"'"
        # cursor.execute("Select EmployeeName,Password from  EmployeeRegistration WHERE  EmployeeName = ? AND  Password = ?",EmployeeName,ENpassword)
        cursor.execute(sql)
        rs=cursor.fetchone()
       

        request.session['EmployeeName']=EmployeeName
        user=request.session['EmployeeName']
           

        if rs is not None:
            # cursor.execute("select TableNo from R_Table")
            # tb=cursor.fetchall()
            return render(request,'index4.html',{'user':user})
        else:
            return render(request,'Login1.html')
          
    else:
        messages.info(request,'Invalid Credential')
        return render(request,'Login1.html')
    

def lgp(request):
	return render(request,'Login1.html')




def TableView(request):
    if 'EmployeeName' not in request.session:
        return render(request,'Login1.html')
    if request.session.has_key:
        ans=request.session['EmployeeName']
        cursor=conn.cursor()
        tb = cursor.execute("select TableNo from R_Table")
        
        # user=request.session['TableName']
        
        cursor=conn.cursor()
        cursor.execute("SELECT rtrim(R_Table.TableNo) as tableNo,BkColor,R_Table.Available,Sum(Case when KOT_Status Not in ('Closed','Void') then GrandTotal else NULL end) as Amt, Max(Case when KOT_Status Not in ('Closed','Void') then Convert(nvarchar(20),DateDiff(Minute,(BillDate),GetDate()))+' Min' else NULL end) as Tm,max(Case when KOT_Status Not in ('Closed','Void') then id else NULL end) as id,R_table.NoOfChairs as totChairs, Sum(Case when KOT_Status Not in ('Closed','Void') then RestaurantPOS_OrderInfoKOT.NoOfPax else 0 end) as NoOfChairsbooked,Count(RestaurantPOS_OrderInfoKOT.ID) as NoOfBill, R_table.NoOfChairs - Sum(Case when KOT_Status Not in ('Closed','Void') then RestaurantPOS_OrderInfoKOT.NoOfPax else 0 end) as vacantchair From R_Table left Join RestaurantPOS_OrderInfoKOT On R_Table.TableNo=Left(RestaurantPOS_OrderInfoKOT.TableNo, Len(RTrim(RestaurantPOS_OrderInfoKOT.TableNo)) - 3) And RestaurantPOS_OrderInfoKOT.KOT_Status = 'open'Where R_Table.branchid = 1 And Status ='Activate'group By R_Table.TableNo,BkColor,Available,R_table.NoOfChairs,RestaurantPOS_OrderInfoKOT.TableNo ORDER BY  Left(R_Table.TableNo, PATINDEX('%[0-9]%', R_Table.TableNo)-1),Convert(Int, SUBSTRING(R_Table.TableNo, PATINDEX('%[0-9]%',R_Table.TableNo), Len(R_Table.TableNo)))")
        result=cursor.fetchall()
        print("TableResult:",result)

    return render(request,'TableSelect.html',{'tb':tb,'ans':ans,'result':result})



user=''
def DetailView(request):
    global user
    sam=request.GET.dict()
    print("Tables:",sam)
    for user in sam.values():
        print()
    
    print("user",user)
    
    request.session['TableName'] = user
    if 'EmployeeName' not in request.session:
        return render(request,'Login1.html')
    if request.session.has_key:
        ans=request.session['EmployeeName']
    
    cursor=conn.cursor()
    cursor.execute("select SUM(t2.Quantity) as Quantity,SUM(t2.Amount)as Amount,SUM(t2.VATAmount)as VATAmount,SUM(t2.TotalAmount) as GrandTotal from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+user+"'")
    result=cursor.fetchone()
   
        
    cursor.connection.cursor()
    cursor.execute('EXEC proc_gettableData @tableName=?',user)
    csr=cursor.fetchone()
    

  
   
    cursor.execute("select * from RestaurantPOS_OrderInfoKOT where KOT_Status='open' and Left(RestaurantPOS_OrderInfoKOT.TableNo,Len(RTrim(RestaurantPOS_OrderInfoKOT.TableNo))-3)='Table2'")
    res=cursor.fetchone()


    cursor.connection.cursor()
    cursor.execute('EXEC proc_gettableData @tableName= ?',user)
    rows = cursor.fetchall()

    cursor=conn.cursor()
    cursor.execute("Select * from Dish d1 inner join SpecialMenu s1 on d1.DishID=s1.Id")
    gallery=cursor.fetchall()


    cursor=conn.cursor()
    # cursor.execute("select * from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT  t2 on (t1.ID) =t2.TicketID  inner join SpecialOrders so on(so.TicketNo)=t1.TicketNo inner join SpecialMenu sp on (sp.Id )=so.Dish_Id where t1.KOT_Status in('open','Pending') and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+user+"'")

    cursor.execute("select * from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT  t2 on (t1.ID) =t2.TicketID  inner join SpecialOrders so on(so.TicketNo)=t1.TicketNo inner join SpecialMenu sp on (sp.Id )=so.Dish_Id where t1.KOT_Status in('open')and so.Status in('Pending') and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+user+"'")
    Special=cursor.fetchall()
    print("special:",Special)
    for row in Special:
        totlqty=row[48]
        print("qqqqqqqtwy:",totlqty)

        Specltot=result[0]+totlqty
        print("miud",Specltot)
        conn.commit()
        
    return render (request,'DetailView.html',{'num':user,'result':result,'res':res,'rows':rows,'csr':csr,'gallery':gallery,'Special':Special})
   
        
    
  
    
    

def Feedback(request):
    if 'EmployeeName' not in request.session:
        return render(request,'EmpRegistration.html')
    if request.session.has_key:
        ans=request.session['TableName']
    cursor=conn.cursor()
   
   
    cursor.execute("select * from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+ans+"'")
    result= cursor.fetchone()
    cursor.execute('EXEC proc_gettableData @tableName= ?',ans)
    pro=cursor.fetchall()
    return render(request,'Feedback.html',{'result':result,'ans':ans,'pro':pro})



def FeedbackView(request):
    if 'EmployeeName' not in request.session:
        return render(request,'EmpRegistration.html')
    if request.session.has_key:
        ans = request.session['TableName'] 
    cursor=conn.cursor()
    cursor.execute("select * from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+ans+"'")
    # cursor.execute("select * from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id where t1.KOT_Status='open'")
    res=cursor.fetchone()
    rs=res[1]
    return render(request,'Feedback.html',{'res':res})



def Feedbackinsert(request):
    if 'EmployeeName' not in request.session:
        return render(request,'EmpRegistration.html')
    if request.session.has_key:
        ans = request.session['TableName'] 
    cursor=conn.cursor()
    cursor.execute("select * from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+ans+"'")
    res=cursor.fetchone()

   

    if res is not None:
  
        rs=res[1]
        # Waiter=res[14]
        # operator=res[5]
        Role='Customer'
        Oper='0'
        Wait='0'
        Cust='0'
       
   
        cursor.execute("select COUNT(*) from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+ans+"'")
        dishres=cursor.fetchval()
        cursor.commit()

        cursor=conn.cursor()
        cursor.execute("select SUM(t2.Quantity) as Quantity,SUM(t2.Amount)as Amount,SUM(t2.VATAmount)as VATAmount,SUM(t2.TotalAmount) as GrandTotal from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+ans+"'")
        result=cursor.fetchone()

        cursor.connection.cursor()
        cursor.execute('EXEC proc_gettableData @tableName= ?',ans)
        csr=cursor.fetchone()

  
   
   


        cursor.connection.cursor()
        cursor.execute('EXEC proc_gettableData @tableName= ?',ans)
        rows = cursor.fetchall()

        cursor.execute("select * from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+ans+"'")
        res=cursor.fetchall()

        cursor=conn.cursor()
        cursor.execute("Select * from SpecialMenu")
        gallery=cursor.fetchall()

       
    
    
        conn.commit()

   
        
        if request.method == "POST":
            FoodFeedback=request.POST['FoodFeedback']
            ServiceComment=request.POST['ServiceComment']
            ServiceFeedback=request.POST['ServiceFeedback']
            FoodComment=request.POST['FoodComment']
            
        
            cursor = conn.cursor()
            query = "INSERT INTO FeedbackMaster(TicketNo,TableNo,Operator,Waiter,Customer,FoodFeedback,ServiceFeedback,ServiceComment,FoodComment,RoleType)VALUES(?,?,?,?,?,?,?,?,?,?)"
            cursor.execute(query,(rs,ans,Oper,Wait,Cust,FoodFeedback,ServiceFeedback,ServiceComment,FoodComment,Role))
            conn.commit()
            datacount=0
            for x in range(dishres):
                datacount=datacount+1
                dishstat="dish"+str(datacount)
                dishcomm="dishcomment"+str(datacount)
                Dishid="DishId"+str(datacount)

                DishFeedback=request.POST[dishstat]
                DishComment=request.POST[dishcomm]
                DishId=request.POST[Dishid]
           

                cursor.execute("Select MAX(Id) from FeedbackMaster")
                feedbakMastr=cursor.fetchval()
                conn.commit()

                cursor.execute("Select MAX(Id) from FeedbackMaster")
                feedbakMastr=cursor.fetchval()
                conn.commit()

                query1="INSERT INTO FeedbackDetails(FBId,DishId,DishFeedback,DishComment)VALUES(?,?,?,?)"
                cursor.execute(query1,(feedbakMastr,DishId,DishFeedback,DishComment))
                conn.commit()
        msg=messages.success(request,'Saved successfully...')
         
        return render(request,'DetailViewCompare.html',{'num':ans,'result':result,'res':res,'rows':rows,'csr':csr,'gallery':gallery,'msg':msg})
    else:
        return render(request,'DetailViewCompare.html')
    


def Cancelbtn(request):
    if 'EmployeeName' not in request.session:
        return render(request,'EmpRegistration.html')
    if request.session.has_key:
        user = request.session['EmployeeName'] 
        num= request.session['TableName'] 
        cursor=conn.cursor()
        cursor.execute("select SUM(t2.Quantity) as Quantity,SUM(t2.Amount)as Amount,SUM(t2.VATAmount)as VATAmount,SUM(t2.TotalAmount) as GrandTotal from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+num+"'")
        result=cursor.fetchone()
           

        cursor.connection.cursor()
        cursor.execute('EXEC proc_gettableData @tableName= ?',num)
        csr=cursor.fetchone()

  
   
        cursor.execute("select * from RestaurantPOS_OrderInfoKOT where KOT_Status='open' and Left(RestaurantPOS_OrderInfoKOT.TableNo,Len(RTrim(RestaurantPOS_OrderInfoKOT.TableNo))-3)='Table2'")
        res=cursor.fetchone()


        cursor.connection.cursor()
        cursor.execute('EXEC proc_gettableData @tableName= ?',num)
        rows = cursor.fetchall()

        cursor.execute("select * from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+num+"'")
        res=cursor.fetchall()
        
    
        conn.commit()
    return render(request,'DetailViewCompare.html',{'user':user,'num':num,'result':result,'res':res,'rows':rows,'csr':csr,'Special':Special})



def LogOut(request):
    if 'EmployeeName' not in request.session:
        return render(request,'Login1.html')
    if request.session.has_key:
        del request.session['EmployeeName']
    return redirect('/')

def Page404(request):
    return redirect('/Login1.html')


def ShowTable(request):
    if 'EmployeeName' not in request.session:
        return render(request,'Login1.html')
    if request.session.has_key('EmployeeName'):
        cursor=conn.cursor()
        cursor.execute("Select tableNo from R_Table")
        res=cursor.fetchall()
        # cursor.execute("SELECT rtrim(R_Table.TableNo) as tableNo,BkColor,R_Table.Available,Sum(Case when KOT_Status Not in ('Closed','Void')then GrandTotal else NULL end) as Amt, Max(Case when KOT_Status Not in ('Closed','Void')then Convert(nvarchar(20),DateDiff(Minute,(BillDate),GetDate()))+' Min' else NULL end) as Tm,max(Case when KOT_Status Not in ('Closed','Void') then id else NULL end) as id,R_table.NoOfChairs as totChairs,KOT_Status as Status, Sum(Case when KOT_Status Not in ('Closed','Void')then RestaurantPOS_OrderInfoKOT.NoOfPax else 0 end) as NoOfChairsbooked,Count(RestaurantPOS_OrderInfoKOT.ID)as NoOfBill, R_table.NoOfChairs - Sum(Case when KOT_Status Not in ('Closed','Void')then RestaurantPOS_OrderInfoKOT.NoOfPax else 0 end)as vacantchair From R_Table left Join RestaurantPOS_OrderInfoKOT On R_Table.TableNo=Left(RestaurantPOS_OrderInfoKOT.TableNo,Len(RTrim(RestaurantPOS_OrderInfoKOT.TableNo)) - 3)And RestaurantPOS_OrderInfoKOT.KOT_Status = 'Open'   Where RestaurantPOS_OrderInfoKOT .KOT_Status='open' And R_Table.branchid = 1 And Status ='Activate' group By R_Table.TableNo,KOT_Status,BkColor,Available,R_table.NoOfChairs,RestaurantPOS_OrderInfoKOT.TableNo ORDER BY  Left(R_Table.TableNo, PATINDEX('%[0-9]%', R_Table.TableNo)-1),Convert(Int, SUBSTRING(R_Table.TableNo, PATINDEX('%[0-9]%',R_Table.TableNo), Len(R_Table.TableNo)))")
        cursor.execute("Select TicketNo,BillDate,TableNo , Max(Case when KOT_Status Not in ('Closed','Void')then Convert(nvarchar(20),DateDiff(Minute,(BillDate),GetDate()))+' Min' else NULL end)as Tm,emp.EmployeeName as Waiter from RestaurantPOS_OrderInfoKOT kt inner join EmployeeRegistration emp   on emp.EmpId =kt.Waiter where KOT_Status='Open' group By TicketNo,BillDate,TableNo,EmployeeName")
        result=cursor.fetchall() 
        cursor.execute("Select dishname,Quantity,Orderto,Notes,BillDate,id,status,TicketNo,KotTime,Fdstatus , Max(Case when status Not in ('Closed','Void')then Convert(nvarchar(20),DateDiff(Minute,(BillDate),GetDate()))+' Min' else NULL end)as Tm from (select DishName as dishname,Quantity,TableNo as Orderto,Notes,BillDate, OP_ID as id,Status as status,TicketNo as TicketNo,KotTime,Fdstatus,BranchId,CategoryName from RestaurantPOS_OrderInfoKOT kot inner join RestaurantPOS_OrderedProductKOT pkot on pkot.TicketID=kot.ID  inner join Dish d on d.DishID=pkot.DishID inner join Category c on c.Cat_ID=pkot.Cat_id   union select DishName as dishname,Quantity,ODN as Orderto,Notes,BillDate,OP_ID as id, takot.Status as status,BillNo as TicketNo,KotTime,FdStatus,BranchId,CategoryName from RestaurantPOS_BillingInfoTA ta   inner join RestaurantPOS_OrderedProductBillTA takot on takot.BillID=ta.ID inner join Dish d on d.DishID=takot.DishID inner join Category c on c.Cat_ID=takot.Cat_id) a where a.status='open' group by dishname,Quantity,Orderto,Notes,BillDate,id,status,TicketNo,KotTime,Fdstatus")
        tot=cursor.fetchall()
        global count
        for x in res:
            if count!=x:
                continue        
        count=x
    return render(request,'ShowTable.html',{'user':result,'res':res,'count':count,'total':tot})

def FilterData(request):
    fromdate=request.POST.get('fromdate')
    todate=request.POST.get('todate')
    cursor=conn.cursor()
    cursor.execute("select * from Register where TokenTime between '"+str(fromdate)+"' and '"+str(todate)+"' and status='pending'  ")
    data=cursor.fetchall()
    cursor.execute("select TableNo from R_Table")
    tb=cursor.fetchall()
    return render(request,'index.html',{'data':data,'tb':tb,})
   

def FilterReport(request):
    fromdate=request.POST.get('fromdate')
    todate=request.POST.get('todate')
    status=request.POST.get('status')
    cursor=conn.cursor()
    cursor.execute("select * from Register order by TokenIn DESC")
    user=cursor.fetchall()
    cursor.execute("Select * from Register where Convert(date, TokenTime) >= '"+str(fromdate)+"'  and Convert(date,TokenTime) <= '"+str(todate)+"' and status ='"+str(status)+"'  ")
    data=cursor.fetchall()
    # cursor.execute("Select * from Register where TokenIn between '"+str(fromdate)+"'  and '"+str(todate)+"' and status ='"+str(status)+"'  ")
    # data=cursor.fetchall()
    conn.commit()
    return render(request,'FinalReports.html',{'data':data,'user':user})




def ImageGallery(request):
    if 'EmployeeName' not in request.session:
        return render(request,'EmpRegistration.html')
    if request.session.has_key('EmployeeName'):
        cursor=conn.cursor()
        cursor.execute("Select * from Dish d1 inner join SpecialMenu s1 on d1.DishID=s1.Id")
        display=cursor.fetchall()
    return render(request,'SpecialMenu.html',{'display':display})


def SpecialMenu(request,id):
    if 'EmployeeName' not in request.session:
        return render(request,'EmpRegistration.html')
    if request.session.has_key('EmployeeName'):
        cursor=conn.cursor()
        cursor.execute("Select * from SpecialMenu s1 inner join Dish d1 on d1.DishID=s1.Id")
        display=cursor.fetchall()
        cursor.execute("Select * from Dish d1 inner join SpecialMenu s1 on d1.DishID=s1.Id where id= "+str(id))
        user=cursor.fetchall()
        cursor.commit()
    return render(request,'display.html',{'user':user,'display':display})
   
    
    

def Highlight(request):
    if 'EmployeeName' not in request.session:
        return render(request,'EmpRegistration.html')
    if request.session.has_key('EmployeeName'):
        cursor=conn.cursor()
        cursor.execute("Select * from Dish d1 inner join SpecialMenu s1 on d1.DishID=s1.Id")
        user=cursor.fetchall()
        cursor.commit()
    return render(request,'display.html',{'user':user})


def check(request):
    num= request.session['TableName'] 
    cursor=conn.cursor()
    cursor.execute('EXEC proc_gettableData @tableName= ?',num)
    rows=cursor.fetchall()
    cursor.execute("select SUM(t2.Quantity) as Quantity,SUM(t2.Amount)as Amount,SUM(t2.VATAmount)as VATAmount,SUM(t2.TotalAmount) as GrandTotal from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+num+"'")
    result=cursor.fetchone()
    print('answer',result)
    return render(request,'temp.html',{'rows':rows,'result':result})



def CustomerPromotion(request):
    if request.method=="POST":
        CC_ID=request.POST['CC_ID']
        if CC_ID =="":
            cursor=conn.cursor() 
            cursor.execute("Select MAX(CC_ID) FROM CreditCustomer")
            creditcus=cursor.fetchval()
            val=creditcus+1
            num = request.GET.dict()
            key = request.POST.getlist("arr[]")
        
    
            CC_ID=val
            CreditCustomerID="CCUS_"+str(val)
            Name=request.POST['Name'] 
            ContactNo=request.POST['ContactNo']
            Address=request.POST['Address']
            WhatsAppNo=request.POST['WhatsAppNo']
            MobileNo=request.POST['MobileNo']
            EmailId=request.POST['EmailId']
            query="insert into CreditCustomer(CC_ID,CreditCustomerID,Name,ContactNo,Address,WhatsAppNo,MobileNo,EmailId) values(?,?,?,?,?,?,?,?)"
            cursor.execute(query,(CC_ID,CreditCustomerID,Name,ContactNo,Address,WhatsAppNo,MobileNo,EmailId))
            
            ProDate=request.POST['ProDate']
            CouponNo=request.POST['coupon']
            PromotionType=request.POST['PromotionType']
            CouponDiscountPer=request.POST['CouponDiscountPer']
            query1="insert into CustomerPromotion(CC_ID,ProDate,CouponNo,PromotionType,CouponDiscountPer)values(?,?,?,?,?)"
            cursor.execute(query1,(CC_ID,ProDate,CouponNo,str(PromotionType),str(CouponDiscountPer)))
            conn.commit()
            cursor.execute("select * from CreditCustomer")
            task=cursor.fetchall()
            msg=messages.success(request,'Saved Successfully....')
            return render(request,'CustomerPromotion.html',{'task':task,'msg':msg})
        else:
            print("before if",request.method)
            if request.method=="POST":
                CC_ID=request.POST['CC_ID']
                print("id:",CC_ID)
                Name=request.POST['Name'] 
                ContactNo=request.POST['ContactNo']
                Address=request.POST['Address']
                WhatsAppNo=request.POST['WhatsAppNo']
                MobileNo=request.POST['MobileNo']
                EmailId=request.POST['EmailId']
                cursor=conn.cursor()
                try:
                    cursor.execute("UPDATE CreditCustomer SET Name=?,ContactNo=?,Address=?,WhatsAppNo=?,MobileNo=?,EmailId=? where CC_ID=?",Name,ContactNo,Address,WhatsAppNo,MobileNo,EmailId,CC_ID)
                    ProDate=request.POST['ProDate']
                    CouponNo=request.POST['coupon']
                    PromotionType=request.POST['PromotionType']
                    CouponDiscountPer=request.POST['CouponDiscountPer']
                    query1="insert into CustomerPromotion(CC_ID,ProDate,CouponNo,PromotionType,CouponDiscountPer)values(?,?,?,?,?)"
                    cursor.execute(query1,(CC_ID,ProDate,CouponNo,str(PromotionType),str(CouponDiscountPer)))
                    conn.commit()
                    messages.success(request,'Updated sucessfully...')
                except pyodbc.Error as error:
                    messages.warning(request,"Something went wrong:".format(error))
                    print("Failed to update record to database rollback: {}".format(error))
                    conn.rollback()     
        return redirect('/CustomerPromotion')
    else:
        return render(request,'CustomerPromotion.html')
    


def CustomerFilter(request):
    if request.is_ajax():
        amount = request.GET.dict()
        print("Yes i am here")
        month = request.POST['month']
        print(f"Post: {request.POST}",month)
        print("ans:",month)
        cursor=conn.cursor()
        cursor.execute("Select * from CreditCustomer where ContactNo   = ?",month)
        rows=cursor.fetchall()
        print(rows)
        rowarray_list = []
        for row in rows:
            t = (row[0], row[1], row[2], row[3], row[4], row[12], row[6], row[7], row[8], row[9], row[10], row[11], row[12],
            row[13], row[14])      
        print("ajax",t)
        return JsonResponse(t,safe=False)
       
    return render(request,'CustomerPromotion.html',{'rows':rows})



def BuyProducts(request,id):
    cursor=conn.cursor()
    cursor.execute("Select * from SpecialMenu where Id = ? ",id)
    order=cursor.fetchall()
    return render(request,'Orders.html',{'order':order})



def Confirm_Orders(request):
    if request.method=='POST':
        num= request.session['TableName'] 
        cursor=conn.cursor()
        # sqlite_select_query="select * from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT  t2 on (t1.ID) =t2.TicketID    inner join SpecialMenu sp on (sp.Id )=t2.Dish_Id where t1.KOT_Status in('open') and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+num+"'"
        sqlite_select_query=" select * from RestaurantPOS_OrderInfoKOT t1  where t1.KOT_Status in('open')and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+num+"'"
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
      
        Dish_Id=request.POST['DishId']
        SpecialDish=request.POST['Dishname']
        rate=request.POST['Price']
        print("IDDDDD:",rate)
        Status='Confirmed'
        QTY=request.POST['qty']
        GrandTotal=request.POST['tot']
        for row in records:
            print("TicketNo: ", row[1])
            print("Table: ", num)
            
            # print("GrandTotal:" , row[50])
            grnd=str(row[3])
            print("\n")
            tbl=str(num)
            print(tbl)
            Date=datetime.now()
            sqlite_insert_query="insert into SpecialOrders(Dish_Id,TicketNo,SpecialDish,rate,Status,GrandTotal,Special_quantity,Table_Name,Date)values(?,?,?,?,?,?,?,?,?)" 
            cursor.execute(sqlite_insert_query,(Dish_Id,row[1],SpecialDish,rate,Status,GrandTotal,QTY,num,Date))
        conn.commit()
    return redirect('/Display_Order')


def Display_Order(request):
    cursor=conn.cursor()
    num= request.session['TableName'] 
    # sqlSelect=("select * from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT  t2 "
    # "on (t1.ID) =t2.TicketID  inner join SpecialOrders so on(so.TicketNo)=t1.TicketNo inner join SpecialMenu sp "
    # "on (sp.DishId )=so.Dish_Id where t1.KOT_Status in('open','Pending') and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+num+"'")

    # sqlSelect="select * from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT  t2 on (t1.ID) =t2.TicketID  inner join SpecialOrders so on(so.TicketNo)=t1.TicketNo inner join SpecialMenu sp on (sp.Id )=so.Dish_Id where t1.KOT_Status in('open','Pending') and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+num+"'"
    sqlSelect="select * from SpecialOrders where Status='Confirmed' and Table_Name='"+num+"'"
    cursor.execute(sqlSelect)
    order=cursor.fetchall()
    conn.commit()
    return render(request,'ConfirmOrder.html',{'Special':order})


# def Stat(request,id):
#     Confirm_Orders="Confirmed"
#     cursor=conn.cursor()
#     cursor.execute("UPDATE SpecialOrders SET Status = ? WHERE id = ?",Confirm_Orders,id)
#     conn.commit()
#     return redirect('/DetailView')


def Stat(request,id):
    Confirm_Orders="Confirmed"
    cursor=conn.cursor()
    cursor.execute("UPDATE SpecialOrders SET Status = ? WHERE id = ?",Confirm_Orders,id)
    
    global k
    print("NEWAns-------:",k)
    sam=request.GET.dict()
    
    for k in sam.values():
        print("ans:",k)
        print("answer",sam)
    # k =request.GET['tablevalue']
        request.session['TableName'] = k
    if 'EmployeeName' not in request.session:
        return render(request,'Login1.html')
    if request.session.has_key:
        ans=request.session['EmployeeName']
    
        cursor=conn.cursor()
        cursor.execute("select SUM(t2.Quantity) as Quantity,SUM(t2.Amount)as Amount,SUM(t2.VATAmount)as VATAmount,SUM(t2.TotalAmount) as GrandTotal from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+k+"'")
        result=cursor.fetchone()
        print('answer',result)
        
        cursor.connection.cursor()
        cursor.execute('EXEC proc_gettableData @tableName= ?',k)
        csr=cursor.fetchone()

  
   
        cursor.execute("select * from RestaurantPOS_OrderInfoKOT where KOT_Status='open' and Left(RestaurantPOS_OrderInfoKOT.TableNo,Len(RTrim(RestaurantPOS_OrderInfoKOT.TableNo))-3)='Table2'")
        res=cursor.fetchone()


        cursor.connection.cursor()
        cursor.execute('EXEC proc_gettableData @tableName= ?',k)
        rows = cursor.fetchall()

        cursor=conn.cursor()
        cursor.execute("Select * from Dish d1 inner join SpecialMenu s1 on d1.DishID=s1.Id")
        gallery=cursor.fetchall()


        cursor=conn.cursor()
        # cursor.execute("select so.TicketNo,Photo, sm.DishId ,so.Date,so.GrandTotal,TableNo,so.quantity,VATAmount,TotalAmount,Sm.Dish_Name,sm.Rate from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id inner join SpecialMenu sm on(sm.DishId)=t2.Dish_Id inner join SpecialOrders so on(so.Dish_Id)=t2.DishID where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+k+"'")
        # cursor.execute("select * from RestaurantPOS_OrderInfoKOT where KOT_Status='open' and Left(RestaurantPOS_OrderInfoKOT.TableNo,Len(RTrim(RestaurantPOS_OrderInfoKOT.TableNo))-3)='"+k+"'")
        # cursor.execute("select * from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT  t2 "
        # "on (t1.ID) =t2.TicketID  inner join SpecialOrders so on(so.TicketNo)=t1.TicketNo inner join SpecialMenu sp "
        # "on (sp.Id )=so.Dish_Id where t1.KOT_Status in('open','Pending') and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+k+"'")
        # Special=cursor.fetchall()
        # print("special:",Special)
        
        # for row in Special:
        #     totlqty=row[48]
        #     print("qqqqqqqtwy:",totlqty)

        #     Specltot=result[0]+totlqty
        #     print("miud",Specltot)
        conn.commit()
        return render (request,'DetailView.html',{'num':k,'result':result,'res':res,'rows':rows,'csr':csr,'gallery':gallery,'Special':Special})
    else:
        return render(request,'DetailView.html',{'num':k,'result':result,'res':res,'rows':rows,'csr':csr,'gallery':gallery,'Special':Special})
    # return redirect('/DetailView')





# def Cancel(request,id):
#     Cancel_Orders="Cancel"
#     cursor=conn.cursor()
#     cursor.execute("UPDATE SpecialOrders SET Status = ? WHERE id = ?",Cancel_Orders,id)
#     conn.commit()
#     # st=cursor.fetchall()
#     return redirect('/Display_Order')

def Cancel(request,id):
    Confirm_Orders="Cancel"
    cursor=conn.cursor()
    cursor.execute("UPDATE SpecialOrders SET Status = ? WHERE id = ?",Confirm_Orders,id)
    
    global k
    print("NEWAns-------:",k)
    sam=request.GET.dict()
    
    for k in sam.values():
        print("ans:",k)
        print("answer",sam)
    # k =request.GET['tablevalue']
        request.session['TableName'] = k
    if 'EmployeeName' not in request.session:
        return render(request,'Login1.html')
    if request.session.has_key:
        ans=request.session['EmployeeName']
    
        cursor=conn.cursor()
        cursor.execute("select SUM(t2.Quantity) as Quantity,SUM(t2.Amount)as Amount,SUM(t2.VATAmount)as VATAmount,SUM(t2.TotalAmount) as GrandTotal from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+k+"'")
        result=cursor.fetchone()
        print('answer',result)
        
        cursor.connection.cursor()
        cursor.execute('EXEC proc_gettableData @tableName= ?',k)
        csr=cursor.fetchone()

  
   
        cursor.execute("select * from RestaurantPOS_OrderInfoKOT where KOT_Status='open' and Left(RestaurantPOS_OrderInfoKOT.TableNo,Len(RTrim(RestaurantPOS_OrderInfoKOT.TableNo))-3)='Table2'")
        res=cursor.fetchone()


        cursor.connection.cursor()
        cursor.execute('EXEC proc_gettableData @tableName= ?',k)
        rows = cursor.fetchall()

        cursor=conn.cursor()
        cursor.execute("Select * from Dish d1 inner join SpecialMenu s1 on d1.DishID=s1.Id")
        gallery=cursor.fetchall()


        cursor=conn.cursor()
        # cursor.execute("select so.TicketNo,Photo, sm.DishId ,so.Date,so.GrandTotal,TableNo,so.quantity,VATAmount,TotalAmount,Sm.Dish_Name,sm.Rate from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT t2 on  Right(t1.TicketNo,Len(RTrim(t1.TicketNo))-4) =t2.TicketID inner join Dish d1 on(d1.DishID)=t2.Dish_Id inner join SpecialMenu sm on(sm.DishId)=t2.Dish_Id inner join SpecialOrders so on(so.Dish_Id)=t2.DishID where t1.KOT_Status='open' and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+k+"'")
        # cursor.execute("select * from RestaurantPOS_OrderInfoKOT where KOT_Status='open' and Left(RestaurantPOS_OrderInfoKOT.TableNo,Len(RTrim(RestaurantPOS_OrderInfoKOT.TableNo))-3)='"+k+"'")
        # cursor.execute("select * from RestaurantPOS_OrderInfoKOT t1 inner join RestaurantPOS_OrderedProductKOT  t2 "
        # "on (t1.ID) =t2.TicketID  inner join SpecialOrders so on(so.TicketNo)=t1.TicketNo inner join SpecialMenu sp "
        # "on (sp.Id )=so.Dish_Id where t1.KOT_Status in('open','Pending') and Left(t1.TableNo,Len(RTrim(t1.TableNo))-3)='"+k+"'")
        # Special=cursor.fetchall()
        # print("special:",Special)
        
        # for row in Special:
        #     totlqty=row[48]
        #     print("qqqqqqqtwy:",totlqty)

        #     Specltot=result[0]+totlqty
        #     print("miud",Specltot)
        conn.commit()
        return render (request,'DetailView.html',{'num':k,'result':result,'res':res,'rows':rows,'csr':csr,'gallery':gallery,'Special':Special})
    else:
        return render(request,'DetailView.html',{'num':k,'result':result,'res':res,'rows':rows,'csr':csr,'gallery':gallery,'Special':Special})




def NewSpecial(request):  
    amount = request.POST.dict()
    print("Yes :",amount)  
    cursor=conn.cursor()
    cursor.execute("Select * from Dish")
    query=cursor.fetchall()
    cursor.execute("Select * from SpecialMenu")
    menu=cursor.fetchall()
    cursor.execute("Select  Dish_Id  from SpecialMenu ")
    user=cursor.fetchall()
    print("RRR:",user)
    return render(request,'CreateSpecial.html',{'query':query,'menu':menu,'user':user})



def UpdateSpecialMenu(request,id): 
    img=""
    cursor=conn.cursor()
    amount = request.POST.dict()
    print("Yes i am here:",amount)
    for img in amount.values():
        print(img)
        print("gfhfdhjd:",img)
        cursor.execute("UPDATE SpecialMenu SET img = ? WHERE id ="+str(id),img)    
    cursor=conn.cursor()
    cursor.execute("Select * from SpecialMenu where Id ="+str(id))
    user=cursor.fetchall()
    print("Midhun:",user)
    conn.commit()
    return render(request,'FullOrder.html',{'user':user})




def CreateSpecial(request):
    if request.is_ajax():
        amount = request.GET.dict()
        print("Yes i am here")
        month = request.POST['month']
        print(f"Post: {request.POST}",month)
        print("ans:",month)
        cursor=conn.cursor()
        cursor.execute("Select * from Dish where DishID = ?",month)
        rows=cursor.fetchall()
        print(rows)
        rowarray_list = []
        for row in rows:
            t = (row[0], row[1], row[2], row[3], row[4], row[12], row[6], row[7], row[8], row[9], "\static\MenuItemsImage"+row[10], row[11], row[12],
            row[13], row[14])      
        print("ajax",t)
        return JsonResponse(t,safe=False)
    return redirect('/NewSpecial')


def DishSpecial(request):
    cursor=conn.cursor()
    cursor.execute("Select * from SpecialMenu ")
    special=cursor.fetchall()
    return render(request,'CreateSpecial.html',{'special':special})
   



def SpecialInsert(request):
    if request.method=="POST":
        cursor=conn.cursor()
        Dish_Id=request.POST["DId"]
        print("aefsiugiuhg:",Dish_Id)
        # Dish_Name=request.POST["tablevalue"]
        Rate=request.POST["Drate"]
        Description=request.POST["DIshDes"]
        img=request.POST["itemimage"]
        Status='Active'
        print(img)
        cursor.execute("Select DishName from Dish  where DishID=?",Dish_Id)
        Dish_Name=cursor.fetchval()
        print("user:",Dish_Name)
        
        
        query="insert into SpecialMenu(Dish_Id,Dish_Name,Rate,Description,img,Status) values(?,?,?,?,?,?)"
        cursor.execute(query,(Dish_Id,Dish_Name,Rate,Description,img,Status))
        messages.success(request,'Saved sucessfully...')
        conn.commit()
    return redirect('/NewSpecial')

sp=""
def SpecialCheck(request):
    global sp
    # if request.is_ajax():
    amount = request.POST.dict()
    print("Yes i am here:",amount)
    for sp in amount.values():
        print("midhun",sp)
        num=list[sp]
        print("out",num[0])
    return render(request,'FullOrder.html',{'values':sp})

def UploadImage(request,id):
    if request.method=="POST":
        cursor=conn.cursor()
        Description=request.POST["updish"]
        print("wwwwww:",Description)
        cursor.execute("UPDATE SpecialMenu SET Description = ? WHERE id ="+str(id),Description) 
        message.success("upload Sucessfully...")
        cursor.commit()
    return redirect('/UpdateSpecialMenu/'+str(id)+'')

def Deactive(request,id):
    cursor=conn.cursor()
    Status='Deactivate'
    cursor.execute("Update SpecialMenu SET Status=? where Id="+str(id),Status)
    msg=messages.info(request,'Deactivated...')
    cursor.commit()
    return redirect('/CreateSpecial',{'msg':msg})

def Active(request,id):
    cursor=conn.cursor()
    Status='Active'
    cursor.execute("Update SpecialMenu SET Status=? where Id="+str(id),Status)
    msg=messages.success(request,'Activated  Successfully...')
    cursor.commit()
    return redirect('/CreateSpecial',{'msg':msg})

def temp(request):
    return render(request,'temp.html')


def SpecialDish(request):
    if request.is_ajax():
        month = request.POST['month']
        print(f"NEW_DISH: {request.POST}",month)
        print("ans:",month)
        cursor=conn.cursor()
        cursor.execute("Select Dish_Id from SpecialMenu where Dish_Id =?",month)
        special=cursor.fetchall()
        print("REsult:",special)
        # return JsonResponse(special,safe=False)
        return JsonResponse({'special ':special})
    return redirect('/NewSpecial')


def GeneralMenu(request):
    cursor=conn.cursor()
    cursor.execute("Select * from Category")
    General=cursor.fetchall()
    cursor.commit()
    return render(request,'GeneralMenu.html',{'General':General})

def GeneralMenuSelect(request,id):
    user=request.GET.dict()
    print("DIC:",user)
    cursor=conn.cursor()
    cursor.execute("Select * from Dish  where Cat_ID =? ",id)
    menu=cursor.fetchall()
    return render(request,'GeneralMenuItems.html',{'menu':menu})


def GeneralOrder(request,id):
    cursor=conn.cursor()
    cursor.execute("Select * from Dish where DishID=?",id)
    data=cursor.fetchall()
    print("Gerenral:",data)
    return render(request,'GeneralMenuItems.html',{'data':data})


import qrcode
import qrcode.image.svg
from io import BytesIO

def QR(request):
    context = {}
    if request.method == "POST":
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(request.POST.get("qr_text",""), image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        context["svg"] = stream.getvalue().decode()

    return render(request, "page.html", context=context)





 

    
    




    
        
 
 





    


    





      

   
   


   

    
  





    
        

       


























  




    
   
       

        
    

    
  


        
























