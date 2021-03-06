"""coursera_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from core.views import index0, index, index2, index3, index4, index_pass

urlpatterns = [

    url(r'^index/$', index),
    url(r'^index0/$', index0),
    url(r'^index2/$', index2),
    url(r'^index3/$', index3),
    url(r'^index4/$', index4),
    url(r'^index_pass/$', index_pass)

]
