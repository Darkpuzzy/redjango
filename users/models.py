from django.db import models


class ClientProfile(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='First name')
    second_name = models.CharField(max_length=150, verbose_name='Second name')
    birthday = models.DateField(verbose_name='Birthday')
    gender = models.CharField(max_length=30, verbose_name='Gender')
    photo = models.ForeignKey('PhotoClient', null=True, verbose_name='Photo', on_delete=models.PROTECT)


class PhotoClient(models.Model):
    photo = models.ImageField(upload_to='images', verbose_name='Photo', blank=True)
