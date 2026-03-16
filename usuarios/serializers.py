from rest_framework import serializers

class Eventoserializers(serializers.Serializer):
    """
    Validar los datos entrantes (json) Antes de enviarlos a firestore
    """ 
    titulo = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    fecha = serializers.DateTimeField()
    lugar = serializers.CharField()

    def validate_titulo(self, value):
        if len(value) <5:
            raise serializers.ValidationError("El titulo debe tener al menos 5 caracteres")
        return value
    
    def validate_descripcion(self, value):
        if len(value) <25:
            raise serializers.ValidationError("La descripcion debe tener al menos 25 caracteres")
        return value 

    