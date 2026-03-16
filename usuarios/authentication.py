from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth
from proyecto_advaih.Firebase_config import initialize_firebase
import firebase_admin

db = initialize_firebase()

class firebaseAuthentication(BaseAuthentication):
    """
    leer el token JWT del encabezado, lo va a validar con firebase y va a extraer el UID del usuario

    """
    def authenticate(self,request):
        #extraemos el token 
        auth_header = request.META.get('HTPP_AUTHORIZATION') or request.headers.get('Authorization')
        if not auth_header:
            return None #si no hay token
        

        #El token viene "Beater <<Token>>"
        partes = auth_header.split()

        if len(partes) != 2 or partes[0].lower() != 'bearer':
            return None
        
        token = partes[1]


        try:
            #le pido a firebase que valide la firma del token
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            user_profile = db.collection('perfiles').document(uid).get()
            rol = user_profile.to_dict().get('rol', 'persona_natural') if user_profile.exists else 'persona_natural'
            #Usuario
            class FirebaseUser:
                def __init__(self, uid, rol, email):
                    self.uid = uid
                    self.rol = rol
                    self.email = email
                    self.is_authenticated = True

            return(FirebaseUser(uid, rol, email), decoded_token)
        except Exception as e:
            raise AuthenticationFailed(f"Token no es valido o esta expirado: {str(e)}")