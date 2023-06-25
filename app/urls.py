from django.urls import path
from . import hod_views, views, staff_views

urlpatterns = [
    path('', views.home_page, name='home_page'),

    path('login', views.login_page, name='login'),
    path('do_login', views.do_login, name='do-login'),
    path('do_logout', views.do_logout, name='logout'),

    ## Profile ##
    path('profile', views.profile, name='profile'),
    path('profile/update', views.profile_update, name='profile-update'),

    ## HOD ##
    path('hod/home', hod_views.HOME, name='hod_home'),
    path('hod/student/add_student', hod_views.add_student, name='add-student'),
    path('hod/student/view_students', hod_views.view_students, name='view-students'),
    path('hod/student/edit_student/<str:id>', hod_views.edit_student, name='edit-student'),
    path('hod/student/delete_student/<str:id>', hod_views.delete_student, name = 'delete-student'),

    path('hod/course/view_courses', hod_views.view_courses, name='view-courses'),
    path('hod/course/add_course', hod_views.add_course, name='add-course'),

    path('hod/course/view_staffs', hod_views.view_staffs, name='view-staffs'),
    # path('hod/course/add_staff', hod_views.add_staff, name='add-staff'),

    ## Staff ##
    path('staff/home', staff_views.staff_home, name='staff_home'),

    ## Subjects ##
    path('subjects/', views.subjects, name='subjects'),

    ## Student ##
    # path('hod/home', hod_views.HOME, name='hod_home'),
]