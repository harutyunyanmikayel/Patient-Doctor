from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Doctor, PatientTime, Patient
from django.contrib.auth.models import User


def patient_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'patients/register.html', {'error_message': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'patients/register.html', {'error_message': 'Username is already taken'})
        if User.objects.filter(email=email).exists():
            return render(request, 'patients/register.html', {'error_message': 'Email is already registered'})

        user = User.objects.create_user(first_name=name, last_name=surname, username=username, email=email, password=password1)
        user.save()

        patient = Patient.objects.create(name=name, surname=surname, username=username, email=email)
        patient.save()

        return redirect('login')
    else:
        return render(request, 'patients/register.html')


def patient_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            return render(request, 'patients/login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'patients/login.html')


def patient_logout(request):
    logout(request)
    return redirect('main_page')


def main_page(request):
    doctors = Doctor.objects.all()
    return render(request, 'patients/main.html', {'doctors': doctors})


def doctor_page(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    all_appointments = PatientTime.objects.all()
    appointment_slots = doctor.appointment_slots.all()

    return render(request, 'patients/doctor.html', {'appointment_slots': appointment_slots,
                                                    'doctor': doctor, 'all_appointments': all_appointments})


def book_appointment(request, doctor_id, time_id):
    patient_time = get_object_or_404(PatientTime, pk=time_id)
    doctor = Doctor.objects.get(pk=doctor_id)

    if request.method == 'POST':
        doctor.appointment_slots.add(patient_time)

        return redirect('doctor_page', doctor_id=doctor_id)
    else:
        return render(request, 'patients/book.html', {'patient_time': patient_time, 'doctor': doctor})
