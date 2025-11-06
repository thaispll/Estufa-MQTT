from django.contrib import admin
from django.urls import path, include
from  views import LeituraViewSet, AlertaViewSet 
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'leituras', LeituraViewSet) #r: rotas
router.register(r'alertas', AlertaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
]
