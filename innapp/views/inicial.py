# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/acesso/login')
def inicio(request):
    mensagem = 'Olá %s, seja bem-vindo(a)!' % request.user.first_name
    return render(request, 'innapp/inicio.html', {'message': mensagem, 'status': 'info'})


def pagina_nao_encontrada(request):
    return render(request, '404.html')