
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path
from django.urls import path
from rest_framework import permissions
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


schema_view = get_schema_view(
   openapi.Info(
      title="Rest API`s",
      default_version='v1',
      description="This api`s for django",
      license=openapi.License(name="BSD License"),
   ),
   public=True
)

doc_url = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


tokens_url = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


client_url = [
    path('client/', views.ClientCreateList.as_view({'get': 'list', 'post': 'create'})),
    path('client/<int:pk>', views.ClientCreateList.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    # path('client/addimage', views.AddProfileImage.as_view({'get': 'list', 'post': 'create'})),
    # path('client/addimage/<int:pk>', views.AddProfileImage.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
]


test_url = [
    path('test/', views.index),
    path('test/weather', views.Weatherget.as_view({'get': 'retrieve'})),
    path('test/info', views.monitoring)
]

urlpatterns = [
    path('', include(tokens_url)),
    path('', include(client_url)),
    path('', include(test_url))
]
