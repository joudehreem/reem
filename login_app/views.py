from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

# Create your views here.
#render the main page
def index(request):
    return render(request,'index.html')

#check if the user not in session can't tgo to success page
def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': get_user(request.session)
        }
        return render(request,'success.html',context)

#handel request post to registration, and pass data to the method to it there are an error shown a msg and redirect to registration page, else create the data and go to the success
def registration(request):
    if request.method == 'POST':
        errors = User.objects.basic_register(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():   
                messages.error(request, value)    
            return redirect('/')
        else:
            user = create_user(request.POST)
            request.session['user_id'] = user.id
            messages.success(request, "Successfully Registered")
            return redirect('/success')
    return redirect('/')


#handel request post to login by user email, and pass data to the method if there are an error display a msg and redirect to main page, else create the data and go to the success page
def login(request):
    if request.method == 'POST':
        errors = User.objects.basic_login(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        
        user = User.objects.filter(email=request.POST['email']) 
        if user: 
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/success')
        # user = User.objects.get(email=request.POST['email'])
        # request.session['user_id'] = user.id
        messages.success(request, "Successfully logged in")
        return redirect('/success')
    else:
        return redirect('/')

# clear the session of user to logout
def logout(request):
    if request.method=='POST':
        request.session.clear()
        return redirect('/')
    
# def error_register(request):
#     errors = User.objects.basic_register(request.POST)
#     if len(errors) > 0:
#         for key, value in errors.items():   
#             messages.error(request, value)
#         return redirect('/')