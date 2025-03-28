from modeltranslation.translator import TranslationOptions,register
from .models import Doctor, Department, Specialty


@register(Doctor)
class ProductTranslationOptions(TranslationOptions):
    fields = ('bio',)

@register(Department)
class ProductTranslationOptions(TranslationOptions):
    fields = ('department_name',)

@register(Specialty)
class ProductTranslationOptions(TranslationOptions):
    fields = ('specialty_name',)