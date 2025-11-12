import paho.mqtt.client as mqtt
import time
import random 

#configurações
BROKER = "broker.hivemq.com"
PORT = 1883
TOPICO_TEMP = "estufa/temperatura"
TOPICO_UMID = "estufa/umidade"

class SimuladorEstufa:
    def __init__(self):
        self.temperatura = 25.0
        self.umidade = 70.0
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc, properties=None): #rc: código de retorno do MQTT
        if rc == 0:
            print(f"Conectado ao broker MQTT")
        else:
            print(f"Erro ao conectar: {rc}")
    
    def conectar(self):
        self.client.connect(BROKER, PORT, 60)
        self.client.loop_start()

    def simular_dados(self):
        self.temperatura += random.uniform(-0.5, 0.5)
        self.umidade += random.uniform(-2,2)

        self.temperatura = max(15, min(35, self.temperatura))
        self.umidade = max(30, min(95, self.umidade))

    def publicar(self):
        self.simular_dados()

        self.client.publish(TOPICO_TEMP, f"{self.temperatura:.2f}")
        print(f"Temperatura: {self.temperatura:.2f}ºC")

        self.client.publish(TOPICO_UMID, f"{self.umidade:.2f}%")
        print(f"Umidade: {self.umidade:.2f}")
    
    def executar(self):
        """executando o simulador"""
        self.conectar()
        print("Simulador de Estufa iniciado")
        print(f"Broker: {BROKER}: {PORT}\n")
        print(f"Tópicos: {TOPICO_TEMP}, {TOPICO_UMID}\n")

        try:
            while True:
                self.publicar()
                time.sleep(5) #publicação a cada 5 segundos
        except KeyboardInterrupt:
            print("\n\n Simulador parado")
            self.client.loop_stop()
            self.client.disconnect()
            
if __name__ == "__main__":
    sim = SimuladorEstufa()
    sim.executar()
