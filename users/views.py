
from rest_framework import status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ClientCreate, ClientSerializer, StandardResultsSetPagination
from .models import *


# Custom token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['shifr'] = 'РукаРукуМоет'
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


#CRUD for client
class ClientCreateList(viewsets.ModelViewSet):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['birthday', 'gender']

    def get_serializer_class(self): # Отвечает за вид отображения API
        methods = ['POST', 'PUT'] # При данных методах, форма отправки данных или редактирования имеет вид {'mode': int, 'colour': int, 'quantity': int}
        if self.request.method in methods:
            return ClientCreate
        return self.serializer_class


# class AddProfileImage(viewsets.ModelViewSet):
#     queryset = PhotoClient.objects.all()
#     serializer_class = PhotoProfileSerializerCreate
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [DjangoFilterBackend]


# Testing auth
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def index(request):
    contetn = {'You succesfull auth'}
    return Response(contetn)


@api_view(['GET', 'POST'])
def test_index(request):
    if request.method == 'POST':
        pass