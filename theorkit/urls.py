
from django.contrib import admin
from django.urls import path
from .viwes import home

#For uploading media file 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home')
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
