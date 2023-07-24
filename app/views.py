from django.shortcuts import render, redirect, HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import CustomUser, StudentRecord, Message, Contact
from django.contrib import messages
from django.db.models import Q


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
            if user_type == 'ADMIN':                
                return redirect('hod_home')
            elif user_type == 'STAFF':    
                return redirect('staff_home')            
                # return HttpResponse('This Staff page')
            elif user_type == 'STUDENT':                
                return redirect('profile')
            else:
                messages.warning(request, 'Assurez vous que vous faites rentrer bon email et mot de passe')
                return redirect('login')
        else:
            messages.warning(request, 'Assurez vous que vous faites rentrer de bon email et mot de passe')
            return redirect('login')
    return None


# general logout page
def do_logout(request):
    logout(request)
    return redirect('home_page')



# @login_required(login_url='login')
def profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    inboxes = Message.objects.filter(
            Q(destinataire_email=request.user.email) | Q(envoyeur=request.user)
        )
    
    message_total = inboxes.count()
    context = {
        'user': user,
        'message_total': message_total
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



def subjects(request):
    signed_in_user = request.user.username
    records = StudentRecord.objects.filter(student__user__username=signed_in_user)
    
    context = {
        'records': records,
    }

    return render(request, 'users/subjects.html', context)


def contact(request):

    if request.method == 'POST':
        nom_prenom = request.POST.get('nom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        motive_message = request.POST.get('motive_message')
        
        contact = Contact(
            nom_prenom = nom_prenom,
            email = email,
            telephone = telephone,
            motive_message = motive_message
        )

        contact.save()
        messages.success(request, 'Votre message a ete envoye, nous vous contacterons bientot. Merci!')
        return redirect('contact')

    return render(request, 'hod/contact.html')