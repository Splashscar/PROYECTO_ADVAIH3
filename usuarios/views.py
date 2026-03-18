from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import Eventoserializers
from .authentication import firebaseAuthentication
from proyecto_advaih.Firebase_config import initialize_firebase
from firebase_admin import firestore

db = initialize_firebase()

class EventoAPIView(APIView):
    authentication_classes = [firebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        """ Listar todos o uno solo """
        try:
            if id:
                doc = db.collection('proyecto ADVAIH').document(id).get()
                if not doc.exists:
                    return Response({"error": "No encontrado"}, status=404)
                return Response(doc.to_dict())
            
            # Listar todos (aquí podrías poner tu lógica de paginación de antes)
            docs = db.collection('proyecto ADVAIH').where('usuario_id', '==', request.user.uid).stream()
            eventos = [({**doc.to_dict(), "id": doc.id}) for doc in docs]
            return Response(eventos, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def post(self, request):
        """ Crear nuevo evento """
        serializer = Eventoserializers(data=request.data)
        if serializer.is_valid():
            datos = serializer.validated_data
            datos['usuario_id'] = request.user.uid
            datos['fecha_creacion'] = firestore.SERVER_TIMESTAMP
            
            nuevo_doc = db.collection('proyecto ADVAIH').add(datos)
            return Response({"mensaje": "Creado", "id": nuevo_doc[1].id}, status=201)
        return Response(serializer.errors, status=400)

    
    def put(self, request, id=None):
        if not id:
            return Response({"Error": "ID requerido"}, status=400)
        
        serializer = Eventoserializers(data=request.data)
        if serializer.is_valid():
            try:
                doc_ref = db.collection('proyecto ADVAIH').document(id)
                doc_snapshot = doc_ref.get()
                
                if not doc_snapshot.exists:
                    return Response({"Error": "No encontrado"}, status=404)
                
                if doc_snapshot.to_dict().get('usuario_id') != request.user.uid:
                    return Response({"error": "No es tuyo"}, status=403)

                doc_ref.update(serializer.validated_data)
                return Response({"mensaje": "Actualizado"}, status=200)
            except Exception as e:
                return Response({"Error": str(e)}, status=500)
        return Response(serializer.errors, status=400)

    # CORRECCIÓN: 'delete' en minúsculas
    def delete(self, request, id=None):
        if not id:
            return Response({"Error": "ID requerido"}, status=400)
        try:
            doc_ref = db.collection('proyecto ADVAIH').document(id)
            doc_snapshot = doc_ref.get()
            
            if not doc_snapshot.exists:
                return Response({"error": "No encontrado"}, status=404)
            
            if doc_snapshot.to_dict().get('usuario_id') != request.user.uid:
                return Response({"error": "No es tuyo"}, status=403)
            
            doc_ref.delete()
            return Response({"mensaje": "Eliminado"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class EnviarTareasEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        correo = request.data.get("correo")
        uid_usuario = request.user.uid  # porque usas Firebase auth

        try:
            
            tareas_ref = db.collection("api_tareas").where(
                "usuario_id", "==", uid_usuario
            )
            docs = tareas_ref.stream()

            tareas = []
            for doc in docs:
                data = doc.to_dict()
                tareas.append(f"- {data.get('titulo')}")

            if not tareas:
                return Response({"mensaje": "No hay tareas"}, status=200)

            mensaje = "Tus tareas:\n\n" + "\n".join(tareas)

            
            send_mail(
                'Tus tareas',
                mensaje,
                'tu_correo@gmail.com',
                [correo],
                fail_silently=False,
            )

            return Response({"mensaje": "Correo enviado correctamente"}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)