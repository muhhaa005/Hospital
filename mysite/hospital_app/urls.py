from django.urls import path, include
from rest_framework import routers
from .views import (UserProfileViewSet, DoctorCreateAPIView, DoctorListAPIView, DoctorDetailAPIView, PatientCreateAPIView, PatientListAPIView, PatientDetailAPIView,
                    DepartmentListAPIView, DepartmentDetailAPIView, SpecialtyListAPIView, SpecialtyDetailAPIView,
                    AppointmentCreateAPIView, AppointmentListAPIView, AppointmentDetailAPIView,
                    MedicalRecordCreateAPIView, MedicalRecordListAPIView, MedicalRecordDetailAPIView,
                    FeedbackCreateAPIView, FeedbackListAPIView, FeedbackDetailAPIView, WardListAPIView, WardDetailAPIView, WardCreateAPIView,
                    RegisterDoctorView, RegisterPatientView, LoginView, LogoutView)

router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),

    path('doctor/', DoctorListAPIView.as_view(), name='doctor_list'),
    path('doctor/<int:pk>/', DoctorDetailAPIView.as_view(), name='doctor_detail'),
    path('doctor/create/', DoctorCreateAPIView.as_view(), name='doctor_create'),

    path('patient/', PatientListAPIView.as_view(), name='patient_list'),
    path('patient/<int:pk>/', PatientDetailAPIView.as_view(), name='patient_detail'),
    path('patient_create/', PatientCreateAPIView.as_view(), name='patient_create'),

    path('department/', DepartmentListAPIView.as_view(), name='department_list'),
    path('department/<int:pk>/', DepartmentDetailAPIView.as_view(), name='department_detail'),

    path('specialty/', SpecialtyListAPIView.as_view(), name='specialty_list'),
    path('specialty/<int:pk>/', SpecialtyDetailAPIView.as_view(), name='specialty_detail'),

    path('appointment/', AppointmentListAPIView.as_view(), name='appointment_list'),
    path('appointment/<int:pk>/', AppointmentDetailAPIView.as_view(), name='appointment_detail'),
    path('appointment_create/', AppointmentCreateAPIView.as_view(), name='appointment_create'),

    path('medical/', MedicalRecordListAPIView.as_view(), name='medical_list'),
    path('medical/<int:pk>/', MedicalRecordDetailAPIView.as_view(), name='medical_detail'),
    path('medical_create/', MedicalRecordCreateAPIView.as_view(), name='medical_create'),

    path('feed/', FeedbackListAPIView.as_view(), name='feed_list'),
    path('feed/<int:pk>/', FeedbackDetailAPIView.as_view(), name='feed_detail'),
    path('feed_create/', FeedbackCreateAPIView.as_view(), name='feed_create'),

    path('ward/', WardListAPIView.as_view(), name='ward_list'),
    path('ward/<int:pk>/', WardDetailAPIView.as_view(), name='ward_detail'),
    path('ward_create', WardCreateAPIView.as_view(), name='ward_create'),

    path('doctor_register/', RegisterDoctorView.as_view(), name='register_doctor'),
    path('patient_register/', RegisterPatientView.as_view(), name='register_patient'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]