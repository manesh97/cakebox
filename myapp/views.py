from django.shortcuts import render,redirect
from django.views.generic import View
from myapp.models import Cakes
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from myapp.models import Cakes
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework import permissions,authentication


class CakeSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Cakes
        fields="__all__"



# Create your views here.
class CakesView(ViewSet):
    #localhost:8000/api/cakes/
    # method:get

    def list(self,request,*args,**kwargs):
        qs=Cakes.objects.all()
        if "flavour" in request.query_params:
            flvr=request.query_params.get("flavour")
            qs=qs.filter(flavour__iexact=flvr)
        if "shape" in request.query_params:
            s=request.query_params.get("shape")
            qs=qs.filter(shape=s)
        # deserialization
        serializer=CakeSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    # localhost:8000/api/cakes/
    # method:get
    def create(self,request,*args,**kwargs):
        serializer=CakeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
        
    # localhost:8000/api/cakes/
    # method:post
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Cakes.objects.get(id=id)
        serializer=CakeSerializer(qs)
        return Response(data=serializer.data)
       
    # localhost:8000/api/cakes/
    # method:put
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp_obj=Cakes.objects.get(id=id)
        serializer=CakeSerializer(instance=emp_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    # localhost:8000/api/cakes/
    # method:delete
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            Cakes.objects.get(id=id).delete()
            return Response(data="deleted")
        except Exception:
            return Response(data="no matching record found")
        

    @action(methods=["get"],detail=False)
    def flavours(self,request,*args,**kwargs):
        qs=Cakes.objects.all().values_list("flavour",flat=True).distinct()
        return Response(data=qs)   

class CakeViewsetView(ModelViewSet):
    serializer_class=CakeSerializer
    model=Cakes
    queryset=Cakes.objects.all()  
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAdminUser]         
        


    

# Create your views here.
from django import forms

class CakeForm(forms.ModelForm):
    class Meta:
        model=Cakes
        fields="__all__"
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "flavour":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-select"}),
            "shape":forms.TextInput(attrs={"class":"form-control"}),
            "weight":forms.TextInput(attrs={"class":"form-control"}),
            "layer":forms.NumberInput(attrs={"class":"form-control"}),
            "pic":forms.FileInput(attrs={"class":"form-control"})

        }

class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "password1":forms.PasswordInput(attrs={"class":"form-control"})
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))        



class CakeCreateView(View):

    def get(self,request,*args,**kwargs):
        form=CakeForm()
        return render(request,"cake-add.html",{"form":form}) 
    def post(self,request,*args,**kwargs):
        form=CakeForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
           
            return redirect("cake-list")
        return render(request,"cake-add.html",{"form":form}) 
       
class CakeListView(View):
    def get(self,request,*args,**kwargs):
        qs=Cakes.objects.all()
        return render(request,"cake-list.html",{"cakes":qs})   

class CakeDetailView(View):
    def get(self,request,*args,**kwargs):
       
        id=kwargs.get("pk")
        qs=Cakes.objects.get(id=id)
        return render(request,"cake-detail.html",{"cake":qs})  
    
class CakeEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        cake=Cakes.objects.get(id=id)
        form=CakeForm(instance=cake)
        return render(request,"cake-edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        cake=Cakes.objects.get(id=id)
        form=CakeForm(request.POST,instance=cake,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("cake-list")
        return render(request,"cake-edit.html",{"form":form}) 
    
class CakeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Cakes.objects.get(id=id).delete()
        return redirect("cake-list")    
       
    
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        return render(request,"register.html",{"form":form})   

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("cake-list")
        return render(request,"login.html",{"form":form})

def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")        

    



