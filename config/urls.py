"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # пользователи
    path('users/', include(('users.urls', 'users'), namespace='users')),

    # каталог на /catalog/
    path('catalog/', include(('catalog.urls', 'catalog'), namespace='catalog')),

    # блог на /blogs/
    path('blogs/', include(('blogs.urls', 'blogs'), namespace='blogs')),

    # главная -> блог, и ОБЯЗАТЕЛЬНО имя 'home'
    path('', RedirectView.as_view(pattern_name='blogs:post_list', permanent=False), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
