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

    # ... (el método post está bien)

    def put(self, request, id=None):
        if not id:
            return Response({"Error": "Se requiere el ID del evento"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = Eventoserializers(data=request.data)
        if serializer.is_valid():
            datos_validados = serializer.validated_data
            try:
                doc_ref = db.collection('proyecto ADVAIH').document(id)
                doc_snapshot = doc_ref.get() # CORRECCIÓN: Obtener el snapshot
                
                if not doc_snapshot.exists:
                    return Response({"Error": "Evento no encontrado"}, status=status.HTTP_404_NOT_FOUND)
                
                tarea_data = doc_snapshot.to_dict() # CORRECCIÓN: usar doc_snapshot
                
                # CORRECCIÓN: comparar con .uid
                if tarea_data.get('usuario_id') != request.user.uid:
                    return Response(
                        {"error": "No tienes permiso para editar este evento"},
                        status= status.HTTP_403_FORBIDDEN
                    )

                doc_ref.update(datos_validados)
                return Response({"mensaje": "Evento actualizado correctamente"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not id:
            return Response({"Error": "se requiere el id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tarea_ref = db.collection('proyecto ADVAIH').document(id)
            doc_snapshot = tarea_ref.get() # CORRECCIÓN: Obtener el snapshot
            
            if not doc_snapshot.exists:
                return Response({"error": "no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            
            tarea_data = doc_snapshot.to_dict() # CORRECCIÓN: usar doc_snapshot
                
            # CORRECCIÓN: comparar con .uid
            if tarea_data.get('usuario_id') != request.user.uid:
                return Response(
                    {"error": "No tienes permiso para eliminar este evento"},
                    status= status.HTTP_403_FORBIDDEN
                )
            
            tarea_ref.delete()
            return Response({"mensaje": f"Evento {id} eliminado"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)