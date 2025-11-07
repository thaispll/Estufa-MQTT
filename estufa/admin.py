from django.contrib import admin
from .models import Leitura, Alerta
from .views import LeituraViewSet, AlertaViewSet

@admin.register(Leitura)
class LeituraAdmin(admin.ModelAdmin):
    list_display = ('temperatura', 'umidade', 'data_hora')
    list_filter = ('data_hora',)
    ordering = ('-data_hora',)

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'mensagem', 'lido', 'data_hora')
    list_filter = ('tipo', 'lido', 'data_hora')
    ordering= ('-data_hora',)
