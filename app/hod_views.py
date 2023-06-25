from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Promotion, Filiere, Module, Student, Staff, Profile, StudentRecord
from django.contrib import messages


@login_required(login_url='login')
def HOME(request):

    total_etudiant = Student.objects.all().count()
    total_filiere = Filiere.objects.all().count()
    total_staff = Staff.objects.all().count()
    

    # student_male = Student.objects.filter(gender='Male').count()
    # student_female = Student.objects.filter(gender='Femelle').count()
    # teacher_count = Course.objects.filter(proffeseur='').count()

    context = {
        'total_etudiant': total_etudiant,
        'total_filiere': total_filiere,
        'total_staff': total_staff,
    }
    return render(request, 'hod/hod_home.html', context)


def add_student(request):
    filieres = Filiere.objects.all()
    promotions = Promotion.objects.all()

    if request.method == 'POST':
        photo = request.FILES.get('profile_pic')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        username = request.POST.get('username')
        date_de_naissance = request.POST.get('date_de_naissance')
        immatriculation = request.POST.get('immatriculation')
        email = request.POST.get('email')
        password = request.POST.get('password')
        sexe = request.POST.get('sexe')
        filiere_id = request.POST.get('filiere_id')
        classe = request.POST.get('classe')
        promotion_id = request.POST.get('promotion_id')
        telephone_etudiant = request.POST.get('telephone_etudiant')
        telephone_parent = request.POST.get('telephone_parent')
        adresse = request.POST.get('adresse')
        # print(
        #     photo, nom, prenom, username,
        #     date_de_naissance, email, password,
        #     sexe, filiere_id, promotion_id,
        #     telephone_etudiant, classe,
        #     telephone_parent, adresse,
        #     immatriculation
        # )
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email deja choisi par un autre utilisateur')
            return redirect('add-student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Cet identification deja choisi par un autre utilisateur')
            return redirect('add-student')
        else:
            user = CustomUser(
                first_name = nom,
                last_name = prenom,
                username = username,
                email = email,
                user_type = 'STUDENT'
            )
            user.set_password(password)
            user.save()

            filiere = Filiere.objects.get(id=filiere_id)
            promotion = Promotion.objects.get(id=promotion_id)

            student = Student(
                user = user,
                sexe = sexe,
                telephone_etudiant = telephone_etudiant,
                telephone_parent = telephone_parent,
                adresse = adresse,
                image = photo,
                date_de_naissance = date_de_naissance,
                immatriculation = immatriculation,
                classe = classe,
                filiere = filiere,
                promotion = promotion,
            )
            student.save()
            messages.success(request, 'Etudiant ajoute. Veiullez lui communiquer son identifiant et mot de passe')
            return redirect('view-students')

    context = {
        'filieres': filieres,
        'promotions': promotions
    }
    return render(request, 'hod/add_student.html', context)


def view_students(request):
    students = Student.objects.all()
    context = {
        'students': students
    }
    return render(request, 'hod/view_students.html', context)



def edit_student(request, id):
    student = Student.objects.get(id=id)
    filieres = Filiere.objects.all()    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        photo = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        password = request.POST.get('password')
        filiere_id = request.POST.get('filiere_id')
        classe = request.POST.get('classe')
        telephone_etudiant = request.POST.get('telephone_etudiant')
        adresse = request.POST.get('adresse')

        # print(
        #     photo, nom, prenom, username,
        #     email, password,
        #     filiere_id,
        #     telephone_etudiant, classe,
        #     adresse, student_id
        # )

        user = CustomUser.objects.get(id=student_id)
        
        user.username = username
        user.first_name = nom
        user.last_name = prenom
        user.email = email
        if password != None and password != '':
            user.set_password(password)
        user.save()

        student = Student.objects.get(user=student_id)
        student.telephone_etudiant = telephone_etudiant
        student.adresse = adresse

        if photo != None and photo != '':
            student.image = photo
        
        student.classe = classe

        filiere = Filiere.objects.get(id=filiere_id)
        student.filiere = filiere

        student.save()

#         promotion = Promotion.objects.get(id=session_year_id)
#         student.session_year = promotion

#         student.save()
        messages.success(request, 'Etudiant est modifie')
        return redirect('view-students') # Change to modified profile

        # student.admin.profile_pic = profile_pic
        # student.address = adresse
        # student.gender = gender
        # student.course_id = 

        # print(profile_pic, username, nom, prenom, email,
        #       gender, course_id, session_year_id,telephone,adresse)
        # student.admin.username = username
        # student.admin.first_name = nom
        # student.admin.last_name = prenom
        # student.admin.email = email
        # student.admin.profile_pic = profile_pic
        # student.address = adresse
        # student.gender = gender
        # student.course_id = 

    context = {
        'student': student,
        'filieres': filieres,
    }
    return render(request, 'hod/edit_student.html', context)


def delete_student(request, id):
    # student = CustomUser.objects.get(id=id)

    student = Student.objects.get(id=id)
    print(student)
    student.delete()
    # messages of name of student deleted
    return redirect('view-students')

def view_courses(request):
    filieres = Filiere.objects.all()
    context = {
        'courses': filieres
    }
    return render(request, 'hod/view_courses.html', context)

def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course = Filiere(
            name=course_name
        )
        course.save()
        print(course_name)
        # messages
        return redirect('view-courses')
    return render(request, 'hod/add_course.html')


def view_staffs(request):
    staffs = Staff.objects.all()
    context = {
        'staffs': staffs
    }
    return render(request, 'hod/view_staffs.html', context)

# def add_staff(request):
#     if request.method == 'POST':
#         profile_pic = request.FILES.get('profile_pic')
#         address = request.POST.get('adresse')
#         nom = request.POST.get('nom')
#         prenom = request.POST.get('prenom')
#         email = request.POST.get('email')
#         telephone = request.POST.get('telephone')
#         sexe = request.POST.get('sexe')
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         print(profile_pic, address, email, nom, prenom, username, password, telephone, sexe)
#         if CustomUser.objects.filter(email=email).exists():
#             messages.warning(request, 'Email deja choisi par un autre utilisateur')
#             return redirect('add-staff')
#         if CustomUser.objects.filter(username=username).exists():
#             messages.warning(request, 'Identification deja choisi par un autre utilisateur')
#             return redirect('add-staff')
#         else:
#             user = CustomUser(
#                 first_name = nom,
#                 last_name = prenom,
#                 email = email,
#                 username = username,
#                 profile_pic = profile_pic,
#                 user_type = 2                
#             )
#             user.set_password(password)
#             user.save()

#             staff = Staff(
#                 admin = user,
#                 address = address,
#                 gender = sexe,
#                 telephone = telephone
#             )
#             staff.save()
#             messages.success(request, f"{nom} {prenom} Veuillez lui communiquer son identifiant et mot de passe")
#             return redirect('view-staffs')
#     return render(request, 'hod/add_staff.html')