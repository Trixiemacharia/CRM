from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    record = Record.objects.all()
    #check to see the logging in
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    #authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'You have been logged in')
            return redirect('home')
        else:
            messages.error(request,'There was an error logging in')
            return redirect('home')
        
    else:
       return render(request, 'home.html', {'records':record})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, 'you have been logged out')
    return render(request, 'home.html')

def register_user(request):
    
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and login
            username= form.cleaned_data['username']
            password= form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "you have signed up successfully")
            return redirect('home')
        else:
            #form is invalid--show form with errors
            return render(request, 'register.html', {'form':form })
    else:
        #GET request --show empty form
        form = SignUpForm
        return render(request, 'register.html', {'form':form})
    
def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
      delete_it = Record.objects.get(id=pk) #get applies filters so the selected record is the one that gets deleted
      delete_it.delete()
      messages.success(request,'Record deleted successfully')
      return redirect('home')
    else:
        messages.success(request,"You must be logged in")
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
           if form.is_valid():
            add_record= form.save()
            messages.success(request,"Record Added")
            return redirect('home')
           return redirect(request, 'add_record.html', {'form': form})
        else:
            messages.success(request,"You must be logged in.")
            return redirect('home')


def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')


