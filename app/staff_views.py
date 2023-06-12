from django.shortcuts import render, redirect

def staff_home(request):
    return render(request, 'staff/staff_home.html')