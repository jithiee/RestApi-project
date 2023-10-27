from django.contrib import admin
from .models import UserCustomModel,Doctor
# Register your models here.

@admin.register(UserCustomModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','password','is_doctor']

