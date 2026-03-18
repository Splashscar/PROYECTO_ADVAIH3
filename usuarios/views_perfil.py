import cloudinary
import cloudinary.uploader

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from .authentication import firebaseAuthentication
from proyecto_advaih.Firebase_config import initialize_firebase

# 🔥 INICIALIZAR FIREBASE CORRECTAMENTE
db = initialize_firebase()

# ==============================
# 🔹 VALIDACIÓN DE IMAGEN
# ==============================

def validar_imagen(file):
    formatos_permitidos = ['image/jpeg', 'image/png', 'image/webp']
    
    if file.content_type not in formatos_permitidos:
        return False, "Formato no permitido. Usa JPG, PNG o WEBP"
    
    if file.size > 5 * 1024 * 1024:  # 5MB
        return False, "La imagen supera el tamaño máximo de 5MB"
    
    return True, None

# ==============================
# 🔹 API CLASE (PRO)
# ==============================

class PerfilImagenAPIView(APIView):
    authentication_classes = [firebaseAuthentication]  # ✅ corregido
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file_to_upload = request.FILES.get('imagen')

        if not file_to_upload:
            return Response(
                {"error": "No se envió ninguna imagen"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔍 Validar imagen
        valido, error = validar_imagen(file_to_upload)
        if not valido:
            return Response({"error": error}, status=400)

        try:
            uid = request.user.uid

            # ☁️ Subir a Cloudinary
            upload_result = cloudinary.uploader.upload(
                file_to_upload,
                folder=f"adso/perfiles/{uid}/",
                public_id="foto_principal",
                overwrite=True
            )

            url_imagen = upload_result.get('secure_url')

            # 🔥 Guardar en Firestore
            doc_ref = db.collection('perfiles').document(uid)

            if doc_ref.get().exists:
                doc_ref.update({'foto_url': url_imagen})
            else:
                doc_ref.set({'foto_url': url_imagen})

            return Response({
                "mensaje": "Foto de perfil actualizada",
                "url": url_imagen
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ==============================
# 🔹 API SIMPLE (OPCIONAL)
# ==============================

@api_view(['POST'])
def subir_foto_perfil(request):

    imagen = request.FILES.get('imagen')

    if not imagen:
        return Response({"error": "No se envió ninguna imagen"}, status=400)

    valido, error = validar_imagen(imagen)
    if not valido:
        return Response({"error": error}, status=400)

    try:
        resultado = cloudinary.uploader.upload(imagen)

        return Response({
            "mensaje": "Imagen subida correctamente",
            "url": resultado.get('secure_url')
        })

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)