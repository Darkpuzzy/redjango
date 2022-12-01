from datetime import datetime

from PIL import Image
from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .cutphoto import crop_center

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
#
#
# class ClientSerializerS(serializers.ModelSerializer):
#
#     class Meta:
#         model = ClientProfile
#         fields = ('first_name', 'second_name', 'birthday', 'gender', 'photo')


# class PhotoProfileSerializerCreate(serializers.ModelSerializer):
#     client = ClientSerializerS()
#
#     class Meta:
#         model = PhotoClient
#         fields = ('client', 'photo', )
#
#     def create(self, validated_data):
#         client = ClientProfile.objects.create(first_name=validated_data.get('client').get('first_name', ''),
#                                               second_name=validated_data.get('client').get('second_name', ''),
#                                               birthday=validated_data.get('client').get('birthday', ''),
#                                               gender=validated_data.get('client').get('gender', '').lower(),)
#         photo = PhotoClient.objects.create(photo=validated_data.get('photo'),
#                                            client_id=client.id)
#         return photo
#
#     def update(self, instance, validated_data):
#         print(instance.client.first_name)
#         try:
#             # instance.client.first_name = validated_data.get('client').get('first_name', instance.client.first_name)
#             # instance.client.second_name = validated_data.get('client').get('second_name', instance.client.second_name)
#             # instance.client.birthday = validated_data.get('client').get('birthday', instance.client.birthday)
#             # instance.client.gender = validated_data.get('client').get('gender', instance.client.gender)
#             instance.photo = validated_data.get('photo',)
#             # instance.client.save()
#             instance.save()
#             return instance
#         except Exception as e:
#             return e


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

        # print(validated_data.get('photo').get('photo',))
        # print(type(validated_data.get('photo').get('photo',)))
        # fp = validated_data.get('photo').get('photo',).image
        # image = Image.open(fp)
        # print(image)
        # cut_photo = crop_center(image)
        # print(cut_photo)
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
            print(p_id)
            try:
                instance.first_name = validated_data.get('first_name', instance.first_name)
                instance.second_name = validated_data.get('second_name', instance.second_name)
                instance.birthday = validated_data.get('birthday', instance.birthday)
                instance.gender = validated_data.get('gender', instance.gender).lower()
                instance.photo_id = p_id
                # instance.photo.photo = validated_data.get('photo').get('photo', instance.photo.photo)
                instance.save()
                # instance.photo.save()
                return instance
            except Exception as e:
                return e