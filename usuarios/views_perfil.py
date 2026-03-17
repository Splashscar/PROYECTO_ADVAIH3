import cloudinary
import cloudinary.uploader
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .authentication import firebaseAuthentication
from proyecto_advaih.Firebase_config import initialize_firebase
from rest_framework.decorators import api_view

db = initialize_firebase

class PerfilImagenAPIView(APIView):
    autentication_classes = [firebaseAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post (self, request):
        file_to_upload = request.FILES.get('imagen')
        if not file_to_upload:
            return Response({"error": "No se envio ninguna imagen"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            uid = request.user.uid

            #1. Subir a cloudinary
            #2. 'FOLDER' nos va a organizar las fotos

            upload_result = cloudinary.uploader.upload(
                file_to_upload,
                folder = f"adso/perfiles/{uid}/",
                public_id="foto_principal",
                overwrite = True
            )

            #2. obtener la url optimizada
            # Cloudinary nos da una url segura HTTPS
            url_imagen = upload_result.get('secure_url')

            #3. Guardar la url en firestore
            db.collection('perfiles').document(uid).update({
                'foto_url': url_imagen
            })
            return Response({
                "mensaje": "Foto de perfil actualizada",
                "url": url_imagen
            }, status = status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        


@api_view(['POST'])
def subir_foto_perfil(request):

    if 'imagen' not in request.FILES:
        return Response({"error": "No se envió ninguna imagen"}, status=400)

    imagen = request.FILES['imagen']

    try:
        resultado = cloudinary.uploader.upload(imagen)

        url_imagen = resultado['secure_url']

        return Response({
            "mensaje": "Imagen subida correctamente",
            "url": url_imagen
        })

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)