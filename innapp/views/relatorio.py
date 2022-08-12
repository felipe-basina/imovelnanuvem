import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from innapp.reports.consultas import recuperar_aluguel_mes_ano
from innapp.utils.utilidades import recuperar_anos_disponiveis


@login_required(login_url='/acesso/login')
def aluguel_mes_ano(request, year=datetime.date.today().year):
    alugueis = recuperar_aluguel_mes_ano(year)

    if not alugueis:
        year = datetime.date.today().year

    current_year = datetime.date.today().year
    available_years = recuperar_anos_disponiveis('aluguel_tbl', 'dt_recebimento')

    # Verifica se o ano atual esta presente na lista, caso contrario, adiciona
    if int(current_year) not in available_years:
        available_years.insert(0, int(current_year))

    template = {
        'all': alugueis,
        'available_years': available_years,
        'selected_year': year
    }

    return render(request, 'innapp/rel-aluguel-mes-ano.html', {'template': template})