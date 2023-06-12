from django.shortcuts import render, redirect, HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import CustomUser


# general home page
def home_page(request):
    return render(request, 'hod/home_page.html')


# general login page
def login_page(request):

    return render(request, 'app/login.html')


# This will determine page to login user
# depending on wheter you're an admin, a staff, or a student
def do_login(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password')
                                         )
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':                
                return redirect('hod_home')
            elif user_type == '2':    
                return redirect('staff_home')            
                # return HttpResponse('This Staff page')
            elif user_type == '3':                
                return HttpResponse('This Student page')
            else:
                # Message
                return redirect('login')
        else:
            # Message
            return redirect('login')
    return None


# general logout page
def do_logout(request):
    logout(request)
    return redirect('home_page')



# @login_required(login_url='login')
def profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        'user': user,
    }
    return render(request, 'users/profile.html', context)

def profile_update(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        # print(profile_pic, nom, prenom, email)
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.profile_pic = profile_pic
            customuser.first_name = nom
            customuser.last_name = prenom
            customuser.email = email
            customuser.save()
            # messages --> Votre info a ete modifie
            return redirect('profile')
        except:
            # messages.error(request, 'Echec! Votre profilen'a pas ete modifie)
            pass
    return render(request, 'users/profile_update.html')