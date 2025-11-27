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
import json
from django.shortcuts import get_object_or_404

class MateriasAll(generics.CreateAPIView):
    #Esta función es esencial para todo donde se requiera autorización de inicio de sesión (token)
    permission_classes = (permissions.IsAuthenticated,)
    # Invocamos la petición GET para obtener todos las materias
    def get(self, request, *args, **kwargs):
        materias = Materias.objects.all().order_by("id")
        lista = MateriaSerializer(materias, many=True).data
        for materia in lista:
            if isinstance(materia, dict) and "dias_json" in materia:
                try:
                    materia["dias_json"] = json.loads(materia["dias_json"])
                except Exception:
                    materia["dias_json"] = []
        return Response(lista, 200)
    
class MateriasView(generics.CreateAPIView):

    def get(self, request, *args, **kwargs):
        materia = get_object_or_404(Materias, id = request.GET.get("id"))
        materia = MateriaSerializer(materia, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(materia, 200)
     
    #Registrar nueva materia
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        print(request.data)
        #Create a profile for the user
        materia = Materias.objects.create(
                                            nrc= request.data["nrc"],
                                            nombre= request.data["nombre"],
                                            seccion= request.data["seccion"],
                                            dias_json = json.dumps(request.data["dias_json"]),
                                            hora_inicio= request.data["hora_inicio"],
                                            hora_final= request.data["hora_final"],
                                            salon= request.data["salon"],
                                            programa_edu= request.data["programa_edu"],
                                            profesor= request.data["profesor"],
                                            creditos= request.data["creditos"])
        materia.save()
        return Response({"materia_created_id": materia.id }, 201)
    # Actualizar datos de la materia
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        #permission_classes = (permissions.IsAuthenticated,)
        # Primero obtenemos la materia a actualizar
        materia = get_object_or_404(Materias, id=request.data["id"])
        materia.nrc = request.data["nrc"]
        materia.nombre = request.data["nombre"]
        materia.seccion = request.data["seccion"]
        materia.dias_json = json.dumps(request.data["dias_json"])
        materia.hora_inicio = request.data["hora_inicio"]
        materia.hora_final = request.data["hora_final"]
        materia.salon = request.data["salon"]
        materia.programa_edu = request.data["programa_edu"]
        materia.profesor = request.data["profesor"]
        materia.creditos = request.data["creditos"]
        materia.save()
        
        return Response({"message": "Materia actualizada correctamente", "materia": MateriaSerializer(materia).data}, 200)
        # return Response(user,200)
        
        #Eliminar materia
    def delete(self, request, *args, **kwargs):
        materia = get_object_or_404(Materias, id=request.GET.get("nrc"))
        try:
            materia.delete()
            return Response({"details":"Materia eliminada"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)

