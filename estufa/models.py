from django.db import models

class Leitura(models.Model):
    """Armazenar leituras de temperatura e umidade"""
    temperatura = models.FloatField()
    #tipo de campo usado em models para armazenar números 
    # com casas decimais
    umidade = models.FloatField()
    data_hora = models.DateTimeField(auto_now_add=True) 
    #adicionar automaticamente 
    class Meta: # por causa do django, metadados (dados adicionais)
        ordering = ['-data_hora']
    
    def __str__(self):
        return f"{self.temperatura}ºC - {self.umidade}% ({self.data_hora})"

class Alerta(models.Model):
    """Armazena alertas de valores críticos"""
    TIPOS = [
        ('TEMP_ALTA', 'Temperatura Alta'),
        ('TEMP_BAIXA', 'Temperatura Baixa'),
        ('UMIDADE_BAIXA', 'Umidade Baixa'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPOS)
    mensagem = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)

    class Meta:
        ordering = ['-data_hora']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.data_hora}"
    