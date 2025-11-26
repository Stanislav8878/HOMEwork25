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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # пользователи
    path('users/', include(('users.urls', 'users'), namespace='users')),

    # каталог
    path('catalog/', include(('catalog.urls', 'catalog'), namespace='catalog')),

    # блог
    path('blogs/', include(('blogs.urls', 'blogs'), namespace='blogs')),

    # рассылки
    path('mailings/', include(('mailings.urls', 'mailings'), namespace='mailings')),

    # главная -> каталог (чтобы там была статистика рассылок)
    path('', RedirectView.as_view(pattern_name='catalog:home', permanent=False), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)