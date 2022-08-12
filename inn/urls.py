"""inny URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path

from innapp.views import imovel, login_logout, inicial, inquilino, aluguel

urlpatterns = [
    path('acc/admin/', admin.site.urls),
    path('imovel/lista', imovel.imovel_todos),
    path('imovel/novo', imovel.imovel_novo),
    path('imovel/<int:idt>', imovel.imovel_por_id),
    path('imovel/edita/<int:idt>', imovel.imovel_edita),
    path('imovel/desativa/<int:idt>', imovel.imovel_desativa),
    path('inquilino/lista', inquilino.inquilino_todos),
    path('inquilino/novo', inquilino.inquilino_novo),
    path('inquilino/<int:idt>', inquilino.inquilino_por_id),
    path('inquilino/edita/<int:idt>', inquilino.inquilino_edita),
    path('inquilino/desativa/<int:idt>', inquilino.inquilino_desativa),
    path('aluguel/lista', aluguel.aluguel_todos),
    path('aluguel/lista/ano/<int:year>', aluguel.aluguel_todos_por_ano),
    path('aluguel/novo', aluguel.aluguel_novo),
    path('aluguel/<int:idt>', aluguel.aluguel_por_id),
    path('aluguel/edita/<int:idt>', aluguel.aluguel_edita),
    path('acesso/login', login_logout.login_user),
    path('acesso/logout', login_logout.logout_user),
    path('', inicial.inicio),
]
