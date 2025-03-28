from django_filters import FilterSet
from .models import Doctor, MedicalRecord

class DoctorFilter(FilterSet):
    class Meta:
        model = Doctor
        fields = {
            'specialty' : ['exact'],
            'department': ['exact'],
        }


class MedicalFilter(FilterSet):
    class Meta:
        model = MedicalRecord
        fields = {
            'patient' : ['exact'],
            'doctor': ['exact'],
        }

