from rest_framework import status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ClientCreate, ClientSerializer, StandardResultsSetPagination, WeatherSerializer
from .models import *


# Custom token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['shifr'] = 'РукаРукуМоет'

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# CRUD for client
# @permission_classes((IsAuthenticated,))
class ClientCreateList(viewsets.ModelViewSet):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['birthday', 'gender']

    # Переопределяем класс serializer для методов POST,PUT
    def get_serializer_class(self):
        methods = ['POST', 'PUT']
        if self.request.method in methods:
            return ClientCreate
        return self.serializer_class


class Weatherget(viewsets.ViewSet):
    serializer_class = WeatherSerializer

    """ Defining the list method to display data unrelated to the model """
    def list(self, request):
        try:
            serializer = WeatherSerializer()
            if serializer.validate(attrs=request.query_params) is True:
                return Response({'Error, please enter the name of city'})
            res = serializer.create(validated_data=request.query_params)
            return Response(res)
        except Exception as e:
            return {'Error': f'{e}'}


# Testing auth
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def index(request):
    contetn = {'You succesfull auth'}
    return Response(contetn)
