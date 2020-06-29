from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login', userlogin, name='userlogin'),
    path('register', register, name='register'),
    path('registeruser', registeruser, name='registeruser'),
    path('validatelogin', validatelogin, name='validatelogin'),
    path('userlogout', userlogout, name='userlogout'),
    path('check_new_jobs',check_new_jobs,name='check_new_jobs')
]