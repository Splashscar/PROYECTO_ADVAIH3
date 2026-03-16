import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth, firestore
from proyecto_advaih.Firebase_config import initialize_firebase

db = initialize_firebase()

class RegistroAPIView(APIView):
    """"""
    authentication_classes= []
    permission_classes=[]

    def post (self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
                return Response ({"Error": "Faltan Credenciales"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user= auth.create_user(email=email, password= password)
            db.collection('perfiles').document(user.uid).set({
                'email' : email,
                'rol':'Persona Natural',
                'Fecha_registro': firestore.SERVER_TIMESTAMP

                })
            return Response({
                    "Mensaje":"Usuario Registrado Correctamente",
                    "uid": user.uid
                }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
                return Response ({"Error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class loginAPIView (APIView):
      authentication_classes=[]
      permission_classes=[]
      def post(self,request):
            email=request.data.get('email')
            password=request.data.get('password')
            api_key= os.getenv('FIREBASE_WEB_API_KEY')
            print(email)
            print(api_key)
        
            if not email or not password:
                    return Response ({"Error": "Faltan credenciales"}, status=status.HTTP_400_BAD_REQUEST)
            
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

            payload ={
                  "email": email,
                  "password": password,
                  "returnSecureToken":True  
            }
            try:
                  
                  response= requests.post(url, json=payload)
                  data= response.json()

                  if response.status_code==200:
                        return Response({
                              "Mensaje": "Login Exitoso",
                              "Token": data['idToken'],
                              "Uid":data['localId']

                        },status=status.HTTP_200_OK)
                  else: 
                        error_msg=data.get('Error', {}).get ('message', 'Error desconocido')
                        return Response ({"Error": error_msg}, status=response.status_code)
            except Exception as e:
                  print (response.status_code)
                  print("="*75)
                  print("\n"+ str(data))
                  return Response ({"Error": "Error de conexion"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)