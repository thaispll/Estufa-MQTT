import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from django.conf import settings
from estufa.models import Leitura, Alerta

class Command(BaseCommand):
    help = "Recebe dados MQTT e salva no banco de dados"

    def __init__(self):
        super().__init__()
        self.temperatura_atual = None #None: ausência de valor
        self.umidade_atual = None
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0: #rc: return code (retorno do código)
            self.stdout.write(self.style.SUCCESS('Conectado ao MQTT'))
            #stdout.write : PRINT SEM A QUEBRA DE LINHA
            client.subscribe("estufa/temperatura")
            client.subscribe("estufa/umidade")
        else: 
            self.stdout.write(self.style.ERROR(f'Erro: {rc}'))
        

    def on_message(self, client, userdata, msg):
        try:
            valor = float(msg.payload.decode())

            if msg.topic == "estufa/temperatura":
                self.temperatura_atual = valor
                self.stdout.write(f"Temperatura: {valor}ºC")

            elif msg.topic == "estufa/umidade":
                self.umidade_atual = valor
                self.stdout.write(f"Umidade: {valor}%")

            #se tivermos os dois valores , salva no banco de dados
            if self.temperatura_atual is not None and self.umidade_atual is not None:
                self.salvar_leitura()
                self.verificar_alertas()
                self.temperatura_atual = None
                self.umidade_atual = None 

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro: {str(e)}"))

    def salvar_leitura(self):
        """Salva a leitura no banco de dados"""
        leitura = Leitura.objects.create(
            temperatura = self.temperatura_atual,
            umidade = self.umidade_atual
        )
        self.stdout.write(self.style.SUCCESS(f"Leitura salva: {leitura}"))
    
    def verificar_alerta(self):
        """Verificar se há valores críticos e criar alertas"""
        if self.temperatura_atual > settings.TEMP_MAX: #comportamento da aplicação
            self.criar_alerta(
                "TEMP_ALTA",
                f"Temperatura {self.temperatura_atual}ºC acima do limite {settings.TEMP_MAX}ºC"
            )
        elif self.temperatura_atual < settings.TEMP_MIN: 
            self.criar_alerta(
                "TEMP_BAIXA",
                f"Temperatura {self.temperatura_atual}ºC abaixo do limite {settings.TEMP_MIN}ºC"
            )

        if self.umidade_atual < settings.UMIDADE_MIN:
            self.criar_alerta(
                "UMIDADE_BAIXA",
                f"Umidade {self.umidade_atual}% abaixo do limite {settings.UMIDADE_MIN}% "
            )
        
        if self.umidade_atual > settings.UMIDADE_MAX:
            self.criar_alerta(
                "UMIDADE_ALTA",
                f"Umidade {self.umidade_atual}% acima do limite {settings.UMIDADE_MAX}% "
            )
        
    def criar_alerta(self, tipo, mensagem):
        alerta = Alerta.objects.create(tipo=tipo, mensagem = mensagem)
        self.stdout.write(self.style.WARNING(f"Alerta: {alerta}"))

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Receptor MQTT Iniciado \n"))

        try:
            self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
            self.client.loop_forever()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\n\n Receptor Parado"))
            self.client.disconnect()

    




        
