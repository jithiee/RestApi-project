
from django.contrib import admin
from django.urls import path,include
from api import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.Register.as_view()),
    path('login/',views.Login.as_view(),name='login'),
    path('userprofile/',views.Userprofile.as_view()),
    path('doctorlist/',views.DoctorsViewlist.as_view()),
    path('adminlist/',views.AdminViewlist.as_view()),
    path('adminlist/<int:pk>/',views.AdminViewlist.as_view()),
]
