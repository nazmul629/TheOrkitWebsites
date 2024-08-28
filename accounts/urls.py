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
    path('my_orders/',my_orders,name='my_orders'),
    path('edit_profile/',edit_profile,name='edit_profile'),
    path('update_password/',update_password,name='update_password'),

    path('orderdetais/<int:order_id>/',order_detail,name='order_detail'),

]