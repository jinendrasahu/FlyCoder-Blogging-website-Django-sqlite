from django.urls import path
from . import views
from django.urls import path,include
urlpatterns = [
    path('postcomment/', views.postcomment,name="postcomment"),
    path('', views.index,name="home"),
    path('contact/', views.contact,name="contact"),
     path('search/', views.search,name="search"),
     path('signup/', views.handlesignup,name="signup"),
     path('login/', views.handlelogin,name="login"),
     path('logout/', views.handlelogout,name="logout"),
     
    path('<str:slug>/', views.blogpost,name="blogpost"),
]
