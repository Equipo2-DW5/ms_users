"""user_ms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from authApp.views import VerifyTokenView, findUser, updateUser, createUser, deleteUser, MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', VerifyTokenView.as_view()),
    path('find/<email>', findUser, name='buscar'),
    path('update/', updateUser, name='actualizar'),
    path('create/', createUser, name='crear'),
    path('delete/', deleteUser, name='borrar'),
]
