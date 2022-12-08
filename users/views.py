from rest_framework import status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ClientCreate, ClientSerializer, StandardResultsSetPagination, WeatherSerializer, MyTokenObtainPairSerializer
from .models import *

from helpers.client import connect_to

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# CRUD for client
@permission_classes((IsAuthenticated,))
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


# Weather API openweathermap.com
# @permission_classes((IsAuthenticated,))
class Weatherget(viewsets.ViewSet):
    serializer_class = WeatherSerializer

    """ Defining the list method to display data unrelated to the model """
    def retrieve(self, request):
        try:
            serializer = self.serializer_class(data=request.query_params)
            if serializer.is_valid():
                data = serializer.data
                res = serializer.create_weather_to_json(validated_data=data)
                return Response(res)
            return Response({'Error, please enter the name of city'})
        except Exception as e:
            return {'Error': str(e)}


# Testing auth
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def index(request):
    contetn = {'You succesfull auth'}
    return Response(contetn)


@api_view(['GET'])
def monitoring(request):
    if request.method == 'GET':
        json_up = connect_to()
        return Response(json_up)
