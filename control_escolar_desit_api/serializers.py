from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=False)
    rol = serializers.CharField(required=False, write_only=True)
    clave_admin = serializers.CharField(required=False, write_only=True, allow_blank=True)
    telefono = serializers.CharField(required=False, write_only=True, allow_blank=True)
    rfc = serializers.CharField(required=False, write_only=True, allow_blank=True)
    edad = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    ocupacion = serializers.CharField(required=False, write_only=True, allow_blank=True)
    confirmar_password = serializers.CharField(required=False, write_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email', 'password', 'rol', 
                  'clave_admin', 'telefono', 'rfc', 'edad', 'ocupacion', 'confirmar_password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'
        
class AlumnoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Alumnos
        fields = "__all__"

class MaestroSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Maestros
        fields = '__all__'

class MateriaSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Materias
        fields = '__all__'