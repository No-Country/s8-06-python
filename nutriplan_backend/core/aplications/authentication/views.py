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
import requests
from django.shortcuts import render

# LOGIN Y REGISTRO
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
    
# BUSQUEDA DE RECETAS

def buscar_recetas(request):
    if request.method == 'GET':
        query = request.GET.get('q', '') 
        app_id = '2a1df3d6'  
        api_key = '44a9edf235f4f291e95637636455047b'  

        url = f'https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            recetas = response.json()['hits']

            # Obtener información nutricional de cada receta
            for receta in recetas:
                recipe_uri = receta['recipe']['uri']
                nutri_app_id = '9e5b7d4c'
                nutri_api_key = '61a30468a7d6ac8b225c357739a9f7df'
                nutricional_url = f'https://api.edamam.com/api/nutrition-details?app_id={nutri_app_id}&app_key={nutri_api_key}'
                payload = {'title': receta['recipe']['label'], 'ingr': receta['recipe']['ingredientLines'], 'uri': recipe_uri}
                nutricional_response = requests.post(nutricional_url, json=payload)
                if nutricional_response.status_code == 200:
                    receta['recipe']['nutritional_info'] = nutricional_response.json()
            
            recetas.sort(key=lambda x: x['recipe']['label'])

            limited_recetas = recetas[:5]  # Limitar a 5 resultados

            print(limited_recetas)
            
            return render(request, 'buscar_recetas.html', {'recetas': limited_recetas})

    return render(request, 'buscar_recetas.html')