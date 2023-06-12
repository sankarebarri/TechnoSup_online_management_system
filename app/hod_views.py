from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Course, SessionYear, Student, Staff
from django.contrib import messages


@login_required(login_url='login')
def HOME(request):

    student_count = Student.objects.all().count()
    course_count = Course.objects.all().count()
    staff_count = Staff.objects.all().count()
    

    # student_male = Student.objects.filter(gender='Male').count()
    # student_female = Student.objects.filter(gender='Femelle').count()
    # teacher_count = Course.objects.filter(proffeseur='').count()

    context = {
        'student_count': student_count,
        'course_count': course_count,
        'staff_count': staff_count,
    }
    return render(request, 'hod/hod_home.html', context)


def add_student(request):
    courses = Course.objects.all()
    session_years = SessionYear.objects.all()

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')
        sexe = request.POST.get('sexe')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

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
                profile_pic = profile_pic,
                user_type = 3

            )
            user.set_password(password)
            user.save()

            course = Course.objects.get(id=course_id)
            session_year = SessionYear.objects.get(id=session_year_id)

            student = Student(
                admin = user,
                address = adresse,
                session_year = session_year,
                course_id = course,
                telephone = telephone,
                gender = sexe
            )
            student.save()
            messages.success(request, 'Etudiant ajoute. Veiullez lui communiquer son identifiant et mot de passe')
            return redirect('view-students')

    context = {
        'courses': courses,
        'session_years': session_years
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
    courses = Course.objects.all()
    session_years = SessionYear.objects.all()
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        # print(student_id)
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        gender = request.POST.get('sexe')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')

        # print("gbbbbfgchbfgc")
        user = CustomUser.objects.get(id=student_id)
        
        # print(user)
        
        user.username = username
        user.first_name = nom
        user.last_name = prenom
        user.email = email
        if profile_pic != None and profile_pic != '':
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin=student_id)
        student.address = adresse
        student.gender = gender
        student.telephone = telephone


        course = Course.objects.get(id=course_id)
        # print(course)
        student.course_id = course

        session_year = SessionYear.objects.get(id=session_year_id)
        student.session_year = session_year

        student.save()
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
        'courses': courses,
        'session_years': session_years
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
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'hod/view_courses.html', context)

def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course = Course(
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

def add_staff(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        address = request.POST.get('adresse')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        sexe = request.POST.get('sexe')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(profile_pic, address, email, nom, prenom, username, password, telephone, sexe)
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email deja choisi par un autre utilisateur')
            return redirect('add-staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Identification deja choisi par un autre utilisateur')
            return redirect('add-staff')
        else:
            user = CustomUser(
                first_name = nom,
                last_name = prenom,
                email = email,
                username = username,
                profile_pic = profile_pic,
                user_type = 2                
            )
            user.set_password(password)
            user.save()

            staff = Staff(
                admin = user,
                address = address,
                gender = sexe,
                telephone = telephone
            )
            staff.save()
            messages.success(request, f"{nom} {prenom} Veuillez lui communiquer son identifiant et mot de passe")
            return redirect('view-staffs')
    return render(request, 'hod/add_staff.html')