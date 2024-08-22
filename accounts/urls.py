from django.urls import path
from.views import *


urlpatterns = [
    path('register/', register, name = "register"),
    path('login/', login, name = "login"),
    path('logout/', logout, name = "logout"),
    path('dashboard/', dashboard, name = "dashboard"),
    path('', dashboard, name = "dashboard"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('forgotPassword/',forgotPassword,name="forgotPassword"),
    path('reset_password/<uidb64>/<token>/', reset_password_validation, name='reset_password_validation'),
    path('resetPassword/',resetPassword,name="resetPassword"),

]