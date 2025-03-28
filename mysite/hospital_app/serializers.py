from rest_framework import serializers
from .models import UserProfile, Doctor, Patient, Department, Specialty, Appointment, MedicalRecord, Feedback, Ward
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'work_day', 'experience', 'department',
                  'shift_start', 'shift_end', 'gender')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Doctor.objects.create_user(**validated_data)
        return user


class UserPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'emergency_contact', 'blood_type', 'profile', 'gender')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Patient.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class DoctorSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name']

class SpecialtySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['specialty_name']

class SpecialtyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'specialty_name']


class DepartmentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name']

class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']


class DoctorListSerializer(serializers.ModelSerializer):
    specialty = SpecialtySimpleSerializer(many=True)
    department = DepartmentSimpleSerializer()
    count_comment = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'specialty', 'department', 'work_day',
                  'count_comment', 'shift_start', 'shift_and', 'service_price', 'role']

    def get_count_comment(self, obj):
        return obj.get_count_comment()


class SpecialtyDetailSerializer(serializers.ModelSerializer):
    doctor_specialty = DoctorListSerializer(many=True, read_only=True)
    class Meta:
        model = Specialty
        fields = ['specialty_name', 'doctor_specialty']


class DepartmentDetailSerializer(serializers.ModelSerializer):
    doctor_department = DoctorListSerializer(many=True, read_only=True)
    class Meta:
        model = Department
        fields = ['department_name', 'level', 'doctor_department']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class PatientSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name']

class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'role']



class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentListSerializer(serializers.ModelSerializer):
    patient = PatientSimpleSerializer()
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'status']

class AppointmentDetailSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    doctor = DoctorSimpleSerializer()
    patient = PatientSimpleSerializer()
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'status', 'date_time']


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'

class MedicalRecordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['id', 'doctor', 'diagnosis']

class MedicalRecordDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format('%d-%m-%Y'))
    doctor = DoctorSimpleSerializer()
    patient = PatientSimpleSerializer()
    class Meta:
        model = MedicalRecord
        fields = ['doctor', 'patient', 'diagnosis', 'treatment', 'prescribed_medication', 'created_at']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class FeedbackListSerializer(serializers.ModelSerializer):
    patient = PatientSimpleSerializer()

    class Meta:
        model = Feedback
        fields = ['id', 'patient', ]

class FeedbackDetailSerializer(serializers.ModelSerializer):
    patient = PatientSimpleSerializer()
    doctor = DoctorSimpleSerializer()

    class Meta:
        model = Feedback
        fields = ['patient', 'doctor', 'comment', 'rating']


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'

class WardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ['id', 'room_number', 'type_ward']

class WardDetailSerializer(serializers.ModelSerializer):
    count_people = serializers.SerializerMethodField()
    class Meta:
        model = Ward
        fields = ['room_number', 'type_ward', 'total_people', 'current_people', 'count_people']

    def get_count_people(self, obj):
        return obj.get_count_people()


class DoctorDetailSerializer(serializers.ModelSerializer):
    specialty = SpecialtySimpleSerializer(many=True)
    department = DepartmentSimpleSerializer()
    appointment_doctor = AppointmentListSerializer(many=True, read_only=True)
    count_comment = serializers.SerializerMethodField()
    doctor_feed = FeedbackListSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialty', 'department', 'work_day', 'bio', 'experience',
                  'doctor_feed', 'count_comment', 'avg_rating', 'appointment_doctor', 'shift_start', 'shift_and', 'service_price', 'role']

    def get_count_comment(self, obj):
        return obj.get_count_comment()

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

class PatientDetailSerializer(serializers.ModelSerializer):
    medical_patient = MedicalRecordListSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'role', 'medical_patient', 'blood_type']
