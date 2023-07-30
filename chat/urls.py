from django.urls import path
from .views import Profilelist,ProfileDetail,Loginpage,RegisterUser,EditProfile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', Profilelist.as_view(), name= 'homeview'),
    path('chat/<str:pk>/', ProfileDetail.as_view(), name='Profile'),
    path('Login/',Loginpage, name ='Loginpage'),
    path('Register', RegisterUser.as_view(), name='Register'),
    path('Logout/', LogoutView.as_view( next_page = 'Loginpage'), name='Logout'),
    path('Edit/<str:pk>/', EditProfile.as_view(), name='Edit')
]