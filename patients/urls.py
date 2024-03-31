from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.patient_register, name='register'),
    path('login/', views.patient_login, name='login'),
    path('logout/', views.patient_logout, name='logout'),
    path('main/', views.main_page, name='main_page'),
    path('doctor/<int:doctor_id>/', views.doctor_page, name='doctor_page'),
    path('doctor/<int:doctor_id>/book/<int:time_id>/', views.book_appointment, name='book_appointment'),
]
