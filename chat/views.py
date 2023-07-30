from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Profile,Chatmodel,Chatnotification
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView,UpdateView
from .forms import UserUpdatedForm,Profileform
from django.urls import reverse_lazy

# Create your views here.
class Profilelist(LoginRequiredMixin, ListView):
    model = Profile
    context_object_name = 'profiles'
    template_name = 'chat/chatpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profiles'] = context['profiles'].exclude(user = self.request.user)
        return context
    
class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'chat/chatuser.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profiles'] = Profile.objects.exclude(user = self.request.user)
        profileid = context['profile'].user.id
        userid = self.request.user.id
        if profileid > userid:
            thread_name = f'{profileid}-{userid}'
        else:
            thread_name = f'{userid}-{profileid}'
        context['chats'] = Chatmodel.objects.filter(thread_name = thread_name)
        context['not'] = Chatnotification.objects.filter(is_seen = False, profile = self.request.user.profile).count()
        
        
        return  context
    
        

def Loginpage(request):
    if request.user.is_authenticated:
        return redirect('homeview')
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')

        try:
            user = User.objects.get(username = username)
        
        except:
            print('user does not exist')
        
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request,user)
            return redirect('homeview')
        else:
            print('password is incorrect')
    
    return render(request,'chat/Loginpage.html')

class RegisterUser(CreateView):
    model = User
    form_class = UserUpdatedForm
    template_name = 'chat/RegisterUser.html'

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
            return redirect('homeview', user.id)
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('homeview')
        return super().get(request, *args, **kwargs)
    

class EditProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'chat/RegisterUser.html'
    success_url = reverse_lazy('homeview')
    form_class = Profileform

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'create-post'
        return context

        




