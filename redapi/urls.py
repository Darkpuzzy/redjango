
from django.contrib import admin
from django.urls import path, include
from users.urls import doc_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('docs/', include(doc_url))
]
