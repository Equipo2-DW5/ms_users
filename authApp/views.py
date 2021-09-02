from authApp.models import labUser
from authApp.serializers import LabUserSerializer, MyTokenObtainPairSerializer
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
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
            serializer.validated_data['email'] = valid_data['email']
            serializer.validated_data['role'] = valid_data['role']
            #pass

        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def findUser(request, email):
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
            if 'role' in request.data.keys():
                usuario.role = request.data["role"]
            if 'state' in request.data.keys():
                usuario.state = request.data["state"]
            usuario.save()
            return Response({"output":"Datos actualizados correctamente"}, status=status.HTTP_200_OK)
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
            return Response({"output":"Ya existe un usuario registrado con este correo"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            if role != "Estudiante":
                usuario = labUser.objects.create_superuser(email=email, first_name=firstName, last_name=lastName, password=password, role=role)
                usuario.save()
                return Response({"output":"Usuario registrado con exito"}, status=status.HTTP_201_CREATED)
            else:
                usuario = labUser.objects.create_user(email=email, first_name=firstName, last_name=lastName, password=password, role='Estudiante')
                usuario.save()
                return Response({"output":"Usuario registrado con exito"}, status=status.HTTP_201_CREATED)
            
@api_view(['POST'])
def deleteUser(request):
    if request.method=='POST':
        email = request.data["email"]
        try:
            usuario = labUser.objects.get(email=email)
            usuario.delete()
            return Response({"output":"Usuario eliminado con exito"}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)