from rest_framework import viewsets, generics, status
from .models import UserProfile, Doctor, Patient, Department, Specialty, Appointment, MedicalRecord, Feedback, Ward
from .serializers import (UserProfileSerializer, DoctorSerializer, DoctorListSerializer, DoctorDetailSerializer, PatientSerializer, PatientListSerializer, PatientDetailSerializer,
                          DepartmentListSerializer, DepartmentDetailSerializer, SpecialtyListSerializer, SpecialtyDetailSerializer, AppointmentSerializer,
                          AppointmentListSerializer, AppointmentDetailSerializer, MedicalRecordSerializer, MedicalRecordListSerializer, MedicalRecordDetailSerializer,
                          FeedbackSerializer, FeedbackListSerializer, FeedbackDetailSerializer, WardListSerializer, WardDetailSerializer, WardSerializer, UserDoctorSerializer, UserPatientSerializer, LoginSerializer
                          )
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions
from .permission import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView



class RegisterDoctorView(generics.CreateAPIView):
    serializer_class = UserDoctorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RegisterPatientView(generics.CreateAPIView):
    serializer_class = UserPatientSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class DoctorCreateAPIView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorListAPIView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DoctorFilter
    ordering_fields = ['service_price']
    permission_classes = [permissions.IsAuthenticated]

class DoctorDetailAPIView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PatientCreateAPIView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientListAPIView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PatientDetailAPIView(generics.RetrieveAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DepartmentListAPIView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['department_name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class DepartmentDetailAPIView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SpecialtyListAPIView(generics.ListAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtyListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['specialty_name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SpecialtyDetailAPIView(generics.RetrieveAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtyDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AppointmentCreateAPIView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckPatient]

class AppointmentListAPIView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['doctor']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AppointmentDetailAPIView(generics.RetrieveAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MedicalRecordCreateAPIView(generics.CreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckDoctor]

class MedicalRecordListAPIView(generics.ListAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filteset_class = MedicalFilter
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

class MedicalRecordDetailAPIView(generics.RetrieveAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FeedbackCreateAPIView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckPatient]

class FeedbackListAPIView(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class FeedbackDetailAPIView(generics.RetrieveAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class WardListAPIView(generics.ListAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['type_ward']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class WardDetailAPIView(generics.RetrieveAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class WardCreateAPIView(generics.CreateAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckPatient]