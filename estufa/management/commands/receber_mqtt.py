import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from django.conf import settings
from estufa.models import Leitura, Alerta