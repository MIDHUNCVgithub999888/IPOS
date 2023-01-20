from unicodedata import name
from django.urls import path,re_path
from. import views
from django.conf.urls import url
from django import urls

from urllib.parse import quote
app_name = 'IposApp'

urlpatterns = [

    path('',views.lgp,name="lgp"),
    path(r'Home/$',views.Home,name="Home"),
    path('Display/',views.Display, name="Display"),
    path(r'Reg/$',views.Reg,name="Reg"),
    path(r'^show/<int:id>/$', views.show, name="show"),
    path(r'^update/<int:id>/$',views.update,name="update"),
    path(r'^report/<int:id>/$',views.report,name="report"),
    path(r'^updt/<int:id>/$',views.updt,name="updt"),
    path(r'^Stat/<int:id>/$',views.Stat,name="Stat"),
    path(r'^FinalReports/',views.FinalReports,name="FinalReports"),
    path(r'^Tables/$',views.Tables,name="Tables"),
    path(r'^log/$',views.log,name="log"),  
    path(r'^TableView/$',views.TableView,name="TableView"),
    path(r'^DetailView/$',views.DetailView,name="DetailView"),
    path(r'^Feedback/$',views.Feedback,name="Feedback"),
    path(r'^FeedbackView/$',views.FeedbackView,name="FeedbackView"),
    path(r'^Cancelbtn/$',views.Cancelbtn,name="Cancelbtn"),
    path(r'^Feedbackinsert/$',views.Feedbackinsert,name="Feedbackinsert"),
    path(r'^LogOut/$',views.LogOut,name="LogOut"),
    path(r'^Page404/$',views.Page404,name="Page404"),
    path(r'^ShowTable/$',views.ShowTable,name="ShowTable"),
    path(r'FilterData/$',views.FilterData,name="FilterData"),
    path('FilterReport/',views.FilterReport,name="FilterReport"),
    path('SpecialMenu/<int:id>/',views.SpecialMenu,name="SpecialMenu"),
    path('Highlight/',views.Highlight,name="Highlight"),
    path('ImageGallery/',views.ImageGallery,name="ImageGallery"),
    path('check/',views.check,name="check"),
    path('CustomerPromotion/',views.CustomerPromotion,name="CustomerPromotion"),
    path('CustomerFilter/',views.CustomerFilter,name="CustomerFilter"),
    path('BuyProducts/<int:id>/',views.BuyProducts,name="BuyProducts"),
    path('Confirm_Orders/',views.Confirm_Orders,name="Confirm_Orders"),
    path('Display_Order/',views.Display_Order,name="Display_Order"),
    path('Stat/<int:id>/',views.Stat,name="Stat"),
    path('Cancel/<int:id>/',views.Cancel,name="Cancel"),
    path('CreateSpecial/',views.CreateSpecial,name="CreateSpecial"),
    path('NewSpecial/',views.NewSpecial,name="NewSpecial"),
    path('SpecialInsert/',views.SpecialInsert,name="SpecialInsert"),
    path('SpecialCheck/',views.SpecialCheck,name="SpecialCheck"),
    path('UpdateSpecialMenu/<int:id>/',views.UpdateSpecialMenu,name="UpdateSpecialMenu"),
    path('UploadImage/<int:id>/',views.UploadImage,name="UploadImage"),
    path('Deactive/<int:id>/',views.Deactive,name="Deactive"),
    path('Active/<int:id>/',views.Active,name="Active"),
    path('DishSpecial/',views.DishSpecial,name="DishSpecial"),
    path('temp/',views.temp,name="temp"),
    path('SpecialDish/',views.SpecialDish,name="SpecialDish"),
    path('Deactive/<int:id>/',views.Deactive,name="Deactive"),
    path('Active/<int:id>/',views.Active,name="Active"),
    path('GeneralMenu/',views.GeneralMenu,name="GeneralMenu"),
    path('GeneralMenuSelect/<int:id>/',views.GeneralMenuSelect,name="GeneralMenuSelect"),
    path('GeneralOrder/<int:id>/',views.GeneralOrder,name="GeneralOrder"),
    path('QR/',views.QR,name="QR"),
    
    
 
 
 
   
]