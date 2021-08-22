from django.http.response import HttpResponse
from authApp.models import labUser
from authApp.serializers import LabUserSerializer
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# Create your views here.
class VerifyTokenView(TokenVerifyView):
    
    def post(self, request, *args, **kwargs):
        token = request.data['token']
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            valid_data = tokenBackend.decode(token, verify=False)
            serializer.validated_data['id'] = valid_data['user_id']
            #pass

        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def findUser(request):
    email = request.data["email"]
    try:
        usuario = labUser.objects.get(email=email)
        serializer = LabUserSerializer(usuario, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except: 
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def updateUser(request):
    if request.method == 'POST':
        email = request.data["email"]
        try:
            usuario = labUser.objects.get(email=email)
            if 'password' in request.data.keys():
                usuario.set_password(request.data["password"])
            if usuario.role == 'Estudiante':
                usuario.save()
                return HttpResponse("Contraseña actualizada correctamente, No puede cambiar más atributos")
            else:
                usuario.role = request.data["role"]
                if 'state' in request.data.keys():
                    usuario.state = request.data["state"]
                usuario.save()
                return HttpResponse("Datos actualizados correctamente")
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def createUser(request):
    if request.method=='POST':
        email = request.data["email"]
        firstName = request.data["first_name"]
        lastName = request.data["last_name"]
        password = request.data["password"]
        role = request.data["role"]
        try:
            usuario = labUser.objects.get(email=email)
            return HttpResponse("Ya existe un usuario registrado con este correo")
        except:
            if role != "Estudiante":
                usuario = labUser.objects.create_superuser(email=email, first_name=firstName, last_name=lastName, password=password, role=role)
                usuario.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                usuario = labUser.objects.create_user(email=email, first_name=firstName, last_name=lastName, password=password, role='Estudiante')
                usuario.save()
                return Response(status=status.HTTP_201_CREATED)
            
@api_view(['POST'])
def deleteUser(request):
    if request.method=='POST':
        email = request.data["email"]
        try:
            usuario = labUser.objects.get(email=email)
            usuario.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)