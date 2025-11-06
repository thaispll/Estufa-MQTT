from django.contrib import admin
from .models import Leitura, Alerta

@admin.register(Leitura)
class LeituraAdmin(admin.ModelAdmin):
    list_display = ('temperatura', 'umidade', 'data_hora')
    list_filter = ('data_hora',)
    ordering = ('-data_hora',)

