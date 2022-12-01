from django.db import models
from django_resized import ResizedImageField


class ClientProfile(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='First name')
    second_name = models.CharField(max_length=150, verbose_name='Second name')
    birthday = models.DateField(verbose_name='Birthday')
    gender = models.CharField(max_length=30, verbose_name='Gender')
    photo = models.ForeignKey('PhotoClient', null=True, verbose_name='Photo', on_delete=models.PROTECT,)


class PhotoClient(models.Model):
    # client = models.ForeignKey(ClientProfile, null=False, verbose_name='Client', on_delete=models.PROTECT)
    # photo = models.ImageField(upload_to='images', verbose_name='Photo', blank=True, null=True)
    photo = ResizedImageField(upload_to='images', verbose_name='Photo', blank=True, null=True, size=[300, 300], crop=['middle', 'center'])
