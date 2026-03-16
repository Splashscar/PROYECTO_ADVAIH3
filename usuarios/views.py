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
    #Traemos nuestro guardia de seguridad
    authentication_classes = [firebaseAuthentication]
    permission_classes = [IsAuthenticated]
    
    """
    ENDPOINT para listar todas las tareas (GET), crear una nueva tarea (POST)
    y actualizar una tarea existente (PUT)
    """

    def get(self, request, tarea_id=None):
        """
        GET: Lista eventos con paginación y control por rol.
        """

        # Obtener límite (máximo 10)
        limit = int(request.query_params.get('Limit', 10))
        if limit > 10:
            limit = 10

        # Obtener cursor de paginación
        last_doc_id = request.query_params.get('last_doc_id')

        uid_usuario = request.user.uid
        rol_usuario = request.user.rol

        try:
            #  Construir query base según rol
            if rol_usuario == 'admin':
                query = db.collection('proyecto ADVAIH')
            else:
                query = db.collection('proyecto ADVAIH') \
                    .where('usuario_id', '==', uid_usuario)

            #  Orden obligatorio para paginación
            query = query.order_by('fecha_creacion')

            #  Aplicar cursor si existe
            if last_doc_id:
                last_doc = db.collection('proyecto ADVAIH').document(last_doc_id).get()
                if last_doc.exists:
                    query = query.start_after(last_doc)

            #  Aplicar límite
            query = query.limit(limit)

            #  Ejecutar consulta UNA sola vez
            docs = query.stream()

            eventos = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                eventos.append(data)

            return Response(
                {
                    "mensaje": f"Listando como rol {rol_usuario}",
                    "limit_aplicado": limit,
                    "cantidad_devuelta": len(eventos),
                    "datos": eventos
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

    def post(self, request):
        serializer = Eventoserializers(data=request.data)
        if serializer.is_valid():
            datos_validados = serializer.validated_data
            
            datos_validados['usuario_id'] = request.user.uid
            datos_validados['fecha_creacion'] = firestore.SERVER_TIMESTAMP
            try:
                #3. guardamos los fatos en firestore
                nuevo_doc = db.collection('proyecto ADVAIH').add(datos_validados)
                id_generado = nuevo_doc[1].id
                return Response({
                    "mensaje": "El evento fue creado correctamente",
                    "id": id_generado
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        """
        Actualiza un evento existente según su ID
        """
        if not id:
            return Response({"Error": "Se requiere el ID del evento"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = Eventoserializers(data=request.data)
        if serializer.is_valid():
            datos_validados = serializer.validated_data
            try:
                doc_ref = db.collection('proyecto ADVAIH').document(id)
                if not doc_ref.get().exists:
                    return Response({"Error": "Evento no encontrado"}, status=status.HTTP_404_NOT_FOUND)
                
                tarea_data = doc.to_dict()
                
                if tarea_data.get('usuario_id') != request.user.id:
                    return Response(
                        {"error": "No tienes permiso para editar este evento"},
                        status= status.HTTP_403_FORBIDDEN
                    )

                doc_ref.update(datos_validados)
                return Response({"mensaje": "Evento actualizado correctamente"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    # eliminar (delet)
    def delete(self, request, id):
        """
        DELETE: eliminar un evento especifico por id, el id viene de la url
        
        """
        if not id:
            return Response({"Error": "se requiere el id de algun evento "}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # referencia al documento 
            tarea_ref = db.collection('proyecto ADVAIH').document(id)
            # verificar que el doc existe antes de borrarlo
            if not tarea_ref.get(). exists:
                return Response({"error": "no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            
            tarea_data = doc.to_dict()
                
            if tarea_data.get('usuario_id') != request.user.id:
                return Response(
                    {"error": "No tienes permiso para editar esta tarea"},
                    status= status.HTTP_403_FORBIDDEN
                )
            
            tarea_ref.delete()
            return Response(
                {"mensaje": f"Evento {id} Se ha eliminado correctamente "},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )