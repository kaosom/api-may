from django.db.models import *
from django.db import transaction
from control_escolar_desit_api.serializers import UserSerializer
from control_escolar_desit_api.serializers import *
from control_escolar_desit_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

class AdminAll(generics.CreateAPIView):
    #Esta función es esencial para todo donde se requiera autorización de inicio de sesión (token)
    permission_classes = (permissions.IsAuthenticated,)
    # Invocamos la petición GET para obtener todos los administradores
    def get(self, request, *args, **kwargs):
        admin = Administradores.objects.filter(user__is_active = 1).order_by("id")
        lista = AdminSerializer(admin, many=True).data
        return Response(lista, 200)

class TotalUsuarios(generics.CreateAPIView):
    #Esta función es esencial para todo donde se requiera autorización de inicio de sesión (token)
    permission_classes = (permissions.IsAuthenticated,)
    # Invocamos la petición GET para obtener el total de usuarios por rol
    def get(self, request, *args, **kwargs):
        total_administradores = Administradores.objects.filter(user__is_active = 1).count()
        total_maestros = Maestros.objects.filter(user__is_active = 1).count()
        total_alumnos = Alumnos.objects.filter(user__is_active = 1).count()
        return Response({
            "administradores": total_administradores,
            "maestros": total_maestros,
            "alumnos": total_alumnos
        }, 200)

class AdminView(generics.CreateAPIView):
    #Obtener usuario por ID
    #permission_classes = (permissions.IsAuthenticated,)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get(self, request, *args, **kwargs):
        admin = get_object_or_404(Administradores, id = request.GET.get("id"))
        admin = AdminSerializer(admin, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(admin, 200)
    
    #Registrar nuevo usuario
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Serializamos los datos del administrador para volverlo de nuevo JSON
        user = UserSerializer(data=request.data)
        
        if user.is_valid():
            #Grabar datos del administrador
            role = request.data.get('rol', 'administrador')
            first_name = request.data.get('first_name', '')
            last_name = request.data.get('last_name', '')
            email = request.data.get('email', '')
            password = request.data.get('password', '')
            
            # Validar que los campos requeridos estén presentes
            if not email or not password or not first_name or not last_name:
                return Response({
                    "message": "Faltan campos requeridos",
                    "errors": {
                        "email": "Este campo es requerido" if not email else None,
                        "password": "Este campo es requerido" if not password else None,
                        "first_name": "Este campo es requerido" if not first_name else None,
                        "last_name": "Este campo es requerido" if not last_name else None,
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
            
            #Valida si existe el usuario o bien el email registrado
            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                return Response({"message":"Username "+email+", is already taken"},400)

            user = User.objects.create( username = email,
                                        email = email,
                                        first_name = first_name,
                                        last_name = last_name,
                                        is_active = 1)


            user.save()
            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            group.save()

            #Almacenar los datos adicionales del administrador
            edad_value = request.data.get("edad")
            if edad_value:
                try:
                    edad_value = int(edad_value) if isinstance(edad_value, str) else edad_value
                except (ValueError, TypeError):
                    edad_value = None
            else:
                edad_value = None
                
            admin = Administradores.objects.create(user=user,
                                            clave_admin= request.data.get("clave_admin", ""),
                                            telefono= request.data.get("telefono", ""),
                                            rfc= request.data.get("rfc", "").upper() if request.data.get("rfc") else "",
                                            edad= edad_value,
                                            ocupacion= request.data.get("ocupacion", ""))
            admin.save()

            return Response({"Admin creado con el ID: ": admin.id }, 201)

        return Response({"message": "Error de validación", "errors": user.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    # Actualizar datos del administrador
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        #permission_classes = (permissions.IsAuthenticated,)
        # Primero obtenemos el administrador a actualizar
        admin = get_object_or_404(Administradores, id=request.data["id"])
        admin.clave_admin = request.data["clave_admin"]
        admin.telefono = request.data["telefono"]
        admin.rfc = request.data["rfc"]
        admin.edad = request.data["edad"]
        admin.ocupacion = request.data["ocupacion"]
        admin.save()
        # Actualizamos los datos del usuario asociado (tabla auth_user de Django)
        user = admin.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()
        
        return Response({"message": "Administrador actualizado correctamente", "admin": AdminSerializer(admin).data}, 200)
        # return Response(user,200)
        
        #Eliminar administrador
    def delete(self, request, *args, **kwargs):
        admin = get_object_or_404(Administradores, id=request.GET.get("id"))
        try:
            admin.user.delete()
            return Response({"details":"Administrador eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)