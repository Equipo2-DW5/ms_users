import json
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from authApp.models import labUser
from django.shortcuts import render
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# Create your views here.
class VerifyTokenView(TokenVerifyView):
    
    def post(self, request, *args, **kwargs):
        token = request.data['token']
        #print(token)
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        serializer = self.get_serializer(data=request.data)
        #print(serializer)
        try:
            serializer.is_valid(raise_exception=True)
            valid_data = tokenBackend.decode(token, verify=False)
            serializer.validated_data['id'] = valid_data['user_id']
            #pass

        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

def findUser(request, email):
    try:
        usuario = labUser.objects.get(email=email)
        return HttpResponse(usuario)
    except: 
    #data = serializers.serialize('json', [usuario,])
        return HttpResponse("No Encontrado")

@csrf_exempt
def updateUser(request):
    if request.method == 'POST':
        try:
            usuario = labUser.objects.get(email=request.POST["email"])
            if 'password' in request.POST.keys():
                usuario.password = request.POST["password"]
            if usuario.role == 'Estudiante':
                usuario.save()
                return HttpResponse("Contraseña actualizada correctamente, No puede cambiar más atributos")
            else:
                usuario.role = request.POST["role"]
                usuario.state = request.POST["state"]
                usuario.save()
                return HttpResponse("Datos actualizados correctamente")
        except:
            print(request.POST["password"])
            return HttpResponse("El usuario no existe")

@csrf_exempt
def createUser(request):
    if request.method=='POST':
        email = request.POST["email"]
        firstName = request.POST["first_name"]
        lastName = request.POST["last_name"]
        password = request.POST["password"]
        role = request.POST["role"]
        try:
            usuario = labUser.objects.get(email=email)
            return HttpResponse("Ya existe un usuario registrado con este correo")
        except:
            if role != "Estudiante":
                usuario = labUser.objects.create_superuser(email=email, first_name=firstName, last_name=lastName, password=password, role=role)
                usuario.save()
                return HttpResponse("Usuario creado correctamente")
            else:
                usuario = labUser.objects.create_user(email=email, first_name=firstName, last_name=lastName, password=password, role='Estudiante')
                usuario.save()
                return HttpResponse("Usuario creado exitosamente")
            
@csrf_exempt
def deleteUser(request):
    if request.method=='POST':
        email = request.POST["email"]
        try:
            usuario = labUser.objects.get(email=email)
            usuario.delete()
            return HttpResponse("Usuario borrado con exito")
        except:
            return HttpResponse("No existe usuario registrado con este email")