from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Album,Song
from django.views.generic import View,CreateView,UpdateView,DeleteView
from .myforms import Mylogin,Register,Addalbum#,Addsong
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request,'music/mainhome1.html')
    else:
        return render(request,'music/mainhome.html')
def index(request):
    a=Album.objects.all()
    if request.user.is_authenticated:
        return render(request,'music/albums1.html',{'album':a})
    else:
        return render(request,'music/albums.html',{'album':a})    

    

def detail(request,pk):
    a=get_object_or_404(Album,pk=int(pk)) 
    context={'val':a}   
    context['user']=request.user
    if request.user.is_authenticated:
        context['master']='music/master1.html'
        return render(request,'music/song.html',context)
    else:
        context['master']='music/master.html'
        return render(request,'music/song.html',context)


    # print(Song.objects.filter(al_id=a))
    return render(request,'music/song.html',{'val':a})
    # if request.user.is_authenticated:
    #     return render(request,'music/song1.html',{'val':a})
    # else:    
    #     return render(request,'music/song.html',{'val':a})

class loginpage(View):
    def get(self,request):
        form=Mylogin(None)
        return render(request,'music/login.html',{'form':form})
    def post(self,request):
        form=Mylogin(request.POST)
        if form.is_valid():
            u=form.cleaned_data['UserName']
            p=form.cleaned_data['Password']
            v=authenticate(username=u,password=p) 
            n=request.GET.get('next',None)  
            if v is not None:
                login(request,v)
                if n:
                    return redirect(n)
                else:    
                    return redirect('music:index')
            return HttpResponse('Logged in '+u)
        return render(request,'music/login.html',{'form':form})         

class signup(CreateView):
    def get(self,request):
        form=Register(None)
        return render(request,'music/register.html',{'form':form})       
    def post(self,request):
        form=Register(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            p=form.cleaned_data['Password']
            data.set_password(p)  
            data.save()
            return redirect('music:login')
        return render(request,'music/register.html',{'form':form})     

def signout(request):
    logout(request)
    return redirect('music:index')

class addalbum(LoginRequiredMixin,View):
    login_url='music:login'
    def get(self,request):
        form=Addalbum(None)
        return render(request,'music/addalbum.html',{'form':form}) 
    def post(self,request):
        form=Addalbum(request.POST,request.FILES)
        form.save()
        return redirect('music:index') 


class updatealbum(LoginRequiredMixin,UpdateView):
    login_url='music:login'
    template_name='music/addalbum.html'
    model=Album
    fields=['title','artist','genre','year','image']
    def form_valid(self,form):
        form.save()
        return redirect('music:index')


class deletealbum(LoginRequiredMixin,DeleteView):
    login_url='music:login'
    template_name='music/delete.html'
    model=Album
    success_url=reverse_lazy('music:index')

class addsong(LoginRequiredMixin,CreateView):
    login_url='music:login'
    template_name='music/addsong.html'
    context_object_name='form'
    model=Song
    fields=['title','artist','genre','sfile','image']
    def form_valid(self,form):  #multiple keyword argument
        i=self.kwargs.get('pk')  #album id
        # print(i)
        a=Album.objects.get(pk=int(i))  #album name
        data=form.save(commit=False)    #song name
        data.al_id=a
        data.save()
        return redirect('music:detail',a.id)    

class updatesong(LoginRequiredMixin,UpdateView):
    login_url='music:login'
    template_name='music/addsong.html'
    context_object_name='form'
    model=Song
    fields=['title','artist','genre','sfile','image']
    def form_valid(self,form):
        form.save()
        print(self.kwargs.get('pk'))
        a=Song.objects.get(id=self.kwargs.get('pk'))
        # print(a)
        return redirect('music:detail',a.al_id.id)

class deletesong(LoginRequiredMixin,DeleteView):
    login_url='music:login'
    template_name='music/delete.html'
    model=Song
    def get_success_url(self):
        a=self.object.al_id
        return reverse_lazy('music:detail',kwargs={'pk':a.id})        

def search(request):
    query=request.GET.get('search')
    print(query)
    if query:
        match=Album.objects.filter(title__contains=query)
        if len(match)!=0:
            return render(request,'music/albums.html',{'album':match})
        else:
            return render(request,'music/searchhome.html')   
    else:
        return render(request,'music/searchhome.html')               


def search1(request):
    query=request.GET.get('search1')
    print(query)
    if query:
        match=Song.objects.filter(title__contains=query)
        if len(match)!=0:
            return render(request,'music/songsearch1.html',{'val':match})
        else:
            return render(request,'music/searchhome1.html')
    else:
        return render(request,'music/searchhome.html')        

def allsongs(request):
    a=Song.objects.all()
    if request.user.is_authenticated:
        return render(request,'music/songsearch1.html',{'val':a})
    else:
        return render(request,'music/songsearch.html',{'val':a})
