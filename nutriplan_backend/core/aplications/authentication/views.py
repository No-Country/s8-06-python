from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserSerializer, RegisterSerializer
from .messages.responses_ok import LOGIN_OK, SIGNUP_OK
from .messages.responses_error import LOGIN_CREDENTIALS_REQUIRED_ERROR, LOGIN_CREDENTIALS_ERROR
from .models import User
from rest_framework.authtoken.models import Token

# Create your views here.
class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    def get(self, request):
        data_response = {"msg": "Método GET no permitido"}
        return Response(data_response, status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        
       
        if email is None or password is None:
            return Response(LOGIN_CREDENTIALS_REQUIRED_ERROR, status=status.HTTP_400_BAD_REQUEST)
        else: 
            try:
                user = User.objects.get(email = email)
                hash_pass = user.password 
                verify_pass = check_password(password, hash_pass)

            except Exception as e:
                print(e)
                verify_pass = False
                
            if verify_pass:

                    token , create = Token.objects.get_or_create(user = user)
                    
                    if create:
                            return Response( {
                            "user": UserSerializer(user, context = self.get_serializer_context()).data,
                            'token': token.key,
                            "message": LOGIN_OK,
                            }, status=status.HTTP_200_OK)
                    else:
                        token.delete()
                        token = Token.objects.create(user=user)
                        return Response( {
                        "user": UserSerializer(user, context = self.get_serializer_context()).data,
                        'token': token.key,
                        "message": LOGIN_OK,
                        }, status=status.HTTP_200_OK)
                
               
            else:
                return Response(LOGIN_CREDENTIALS_ERROR, status=status.HTTP_401_UNAUTHORIZED)
class SignUpView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user, context = self.get_serializer_context()).data,
                "message": SIGNUP_OK
            },
        )
class LogoutView(APIView):
    
    def post(self, request):
        email = request.data['email']
        try:
            user = User.objects.get(email = email)
            token = Token.objects.get(user = user)
            token.delete()
            data = {'code': 200, 'msg': 'Sesión cerrada'}
            code = status.HTTP_200_OK
        except:
            data = {'code': 401, 'msg': 'Credenciales incorrectas'}
            code = status.HTTP_401_UNAUTHORIZED
        return Response(data, status = code)