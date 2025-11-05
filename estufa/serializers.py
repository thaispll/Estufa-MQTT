#serializer: componentes fundamentais
# que convertem dados complexos e formatos simples
# que podem ser recebidos em APIs REST
#Converter objetos Python em formato nativo (JSON, XML)
#para envios de respostas HTTP

from rest_framework import serializers
from .models import Leitura, Alerta

class LeituraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leitura
        fields = ['id', 'temperatura', 'umidade', 'data_hora']

class AlertaSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only = True)

    class Meta:
        model = Alerta
        fields = ['id', 'tipo', 'tipo_display', 'mensagem', 'data_hora', 'lido']