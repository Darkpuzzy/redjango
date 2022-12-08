from abc import ABC
from datetime import datetime

from PIL import Image
from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .cutphoto import crop_center
from .weatherapi import WeatherApi

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Pagination classes
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


# CRUD for Client and Photo
class ClientSerializer(serializers.ModelSerializer):
    """Шаблон отображения client для метода запроса GET"""
    class Meta:
        model = ClientProfile
        fields = ('id', 'first_name', 'second_name', 'birthday', 'gender', 'photo')


class PhotoProfileSerializerCreated(serializers.ModelSerializer):
    """ Использование модели Photo для подгрузки файла напрямую { 'phot': [ 'photo': filename ] }"""
    class Meta:
        model = PhotoClient
        fields = ('photo',)


class ClientCreate(serializers.ModelSerializer):
    photo = PhotoProfileSerializerCreated()

    class Meta:
        model = ClientProfile
        fields = ('id', 'first_name', 'second_name', 'birthday', 'gender', 'photo')

    """ Переопределяем валидацию по гендеру """
    def validate(self, attrs):
        gender_list = ['men', 'female']
        model = attrs.get('gender').lower()
        bool = model in gender_list
        if bool is False:
            raise serializers.ValidationError(
                {"Entered men or female"})
        return attrs

    """Переопределяем метод create"""
    def create(self, validated_data):
        """ boolean нужен для проверки photo что бы назначить базовую фотку для client если он не поставит фото """
        # if photo = null, added photo destroyed db and method PUT doesn`t work
        boolean = validated_data.get('photo').get('photo', '') is None
        if boolean:
            client = ClientProfile.objects.create(first_name=validated_data.get('first_name', ''),
                                                  second_name=validated_data.get('second_name', ''),
                                                  birthday=validated_data.get('birthday', ''),
                                                  gender=validated_data.get('gender', '').lower(),
                                                  photo_id=1) # Basic photo client
            return client

        try:
            created_photo = PhotoClient.objects.create(photo=validated_data.get('photo').get('photo',))
            client = ClientProfile.objects.create(first_name=validated_data.get('first_name', ''),
                                                  second_name=validated_data.get('second_name', ''),
                                                  birthday=validated_data.get('birthday', ''),
                                                  gender=validated_data.get('gender', '').lower(),
                                                  photo_id=created_photo.id)

            return client
        except Exception as e:
            return e

    def update(self, instance, validated_data):
        boolean = validated_data.get('photo').get('photo', '') is None
        if boolean:
            try:
                instance.first_name = validated_data.get('first_name', instance.first_name)
                instance.second_name = validated_data.get('second_name', instance.second_name)
                instance.birthday = validated_data.get('birthday', instance.birthday)
                instance.gender = validated_data.get('gender', instance.gender).lower()
                instance.save()
                return instance
            except Exception as e:
                return e
        else:
            photo_id = PhotoClient.objects.create(photo=validated_data.get('photo').get('photo', ))
            p_id = photo_id.id
            photo_id.save()
            try:
                instance.first_name = validated_data.get('first_name', instance.first_name)
                instance.second_name = validated_data.get('second_name', instance.second_name)
                instance.birthday = validated_data.get('birthday', instance.birthday)
                instance.gender = validated_data.get('gender', instance.gender).lower()
                instance.photo_id = p_id
                instance.save()
                return instance
            except Exception as e:
                return e


class WeatherSerializer(serializers.Serializer):

    date = serializers.DateField(required=False)
    city = serializers.CharField(max_length=256)

    def validate(self, attrs):
        boolean = attrs.get('city').isdigit()
        if boolean:
            raise serializers.ValidationError(
                {"Entered city"})
        return attrs

    def create_weather_to_json(self, validated_data):
        try:
            if validated_data.get('date') is None:
                weather = WeatherApi.weather_today(city=validated_data.get('city'))
            else:
                weather = WeatherApi.weather_at_date(city=validated_data.get('city'), date=validated_data.get('date'))

            response = {
                'date': validated_data.get('date'),
                'city': validated_data.get('city'),
                'weather': weather
            }
            return response
        except Exception as e:
            return {'Error': str(e)}


# Custom token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['shifr'] = 'РукаРукуМоет'

        return token
