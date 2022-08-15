import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from innapp.reports.consultas import *
from innapp.utils.utilidades import recuperar_anos_disponiveis


@login_required(login_url='/acesso/login')
def aluguel_mes_ano(request, year=datetime.date.today().year):
    alugueis = recuperar_aluguel_mes_ano(year)
    return render(request,
                  'innapp/rel-mes-ano.html',
                  {'template': relatorio_template(alugueis, year, 'aluguel_tbl', 'dt_recebimento', 'aluguel', 'aluguéis')})


@login_required(login_url='/acesso/login')
def aluguel_ano(request, year=datetime.date.today().year):
    alugueis = recuperar_aluguel_ano()
    return render(request,
                  'innapp/rel-ano.html',
                  {'template': relatorio_template(alugueis, year, 'aluguel_tbl', 'dt_recebimento', 'aluguel', 'aluguéis')})


@login_required(login_url='/acesso/login')
def reforma_mes_ano(request, year=datetime.date.today().year):
    reformas = recuperar_reforma_mes_ano(year)
    return render(request,
                  'innapp/rel-mes-ano.html',
                  {'template': relatorio_template(reformas, year, 'reforma_tbl', 'dt_reforma', 'reforma', 'reformas')})


@login_required(login_url='/acesso/login')
def reforma_ano(request, year=datetime.date.today().year):
    reformas = recuperar_reforma_ano()
    return render(request,
                  'innapp/rel-ano.html',
                  {'template': relatorio_template(reformas, year, 'reforma_tbl', 'dt_reforma', 'reforma', 'reformas')})


@login_required(login_url='/acesso/login')
def administracao_mes_ano(request, year=datetime.date.today().year):
    alugueis = recuperar_administracao_mes_ano(year)
    return render(request,
                  'innapp/rel-mes-ano.html',
                  {'template': relatorio_template(alugueis, year, 'aluguel_tbl', 'dt_recebimento', 'administracao', 'administração')})


@login_required(login_url='/acesso/login')
def administracao_ano(request, year=datetime.date.today().year):
    alugueis = recuperar_administracao_ano()
    return render(request,
                  'innapp/rel-ano.html',
                  {'template': relatorio_template(alugueis, year, 'aluguel_tbl', 'dt_recebimento', 'administracao', 'administração')})


def relatorio_template(registros, ano, tabela, coluna, tipo_registro, tipo_registro_pl):
    current_year = datetime.date.today().year
    available_years = recuperar_anos_disponiveis(tabela, coluna)

    # Verifica se o ano atual esta presente na lista, caso contrario, adiciona
    if int(current_year) not in available_years:
        available_years.insert(0, int(current_year))

    template = {
        'all': registros,
        'available_years': available_years,
        'selected_year': ano,
        'type_reg': tipo_registro,
        'type_reg_pl': tipo_registro_pl
    }

    return template
