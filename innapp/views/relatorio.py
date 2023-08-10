from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from innapp.reports.consultas import *
from innapp.tables import MesAnoTable, AnoTable, PendenteTable, ReformaImovelTable, AluguelImovelTable, \
    PendenteAnoTable, TotalTable
from innapp.utils.utilidades import recuperar_anos_disponiveis


@login_required(login_url='/acesso/login')
def aluguel_mes_ano(request, year=None):
    if year is None:
        year = datetime.date.today().year

    alugueis = recuperar_aluguel_mes_ano(year)
    return render(request,
                  'innapp/rel-mes-ano.html',
                  {'template': relatorio_template(MesAnoTable(converte_para_map(alugueis)),
                                                  year,
                                                  'aluguel_tbl',
                                                  'dt_recebimento',
                                                  'aluguel',
                                                  'aluguéis')})


@login_required(login_url='/acesso/login')
def aluguel_ano(request, year=None):
    if year is None:
        year = datetime.date.today().year

    alugueis = recuperar_aluguel_ano()
    return render(request,
                  'innapp/rel-ano.html',
                  {'template': relatorio_template(AnoTable(converte_para_map(alugueis)),
                                                  year,
                                                  'aluguel_tbl',
                                                  'dt_recebimento',
                                                  'aluguel',
                                                  'aluguéis')})


@login_required(login_url='/acesso/login')
def reforma_mes_ano(request, year=None):
    if year is None:
        year = datetime.date.today().year

    reformas = recuperar_reforma_mes_ano(year)
    return render(request,
                  'innapp/rel-mes-ano.html',
                  {'template': relatorio_template(MesAnoTable(converte_para_map(reformas)),
                                                  year,
                                                  'reforma_tbl',
                                                  'dt_reforma',
                                                  'reforma',
                                                  'reformas')})


@login_required(login_url='/acesso/login')
def reforma_ano(request, year=None):
    if year is None:
        year = datetime.date.today().year

    reformas = recuperar_reforma_ano()
    return render(request,
                  'innapp/rel-ano.html',
                  {'template': relatorio_template(AnoTable(converte_para_map(reformas)),
                                                  year,
                                                  'reforma_tbl',
                                                  'dt_reforma',
                                                  'reforma',
                                                  'reformas')})


@login_required(login_url='/acesso/login')
def administracao_mes_ano(request, year=None):
    if year is None:
        year = datetime.date.today().year

    administracao = recuperar_administracao_mes_ano(year)
    return render(request,
                  'innapp/rel-mes-ano.html',
                  {'template': relatorio_template(MesAnoTable(converte_para_map(administracao)),
                                                  year,
                                                  'aluguel_tbl',
                                                  'dt_recebimento',
                                                  'administracao',
                                                  'administração')})


@login_required(login_url='/acesso/login')
def administracao_ano(request, year=None):
    if year is None:
        year = datetime.date.today().year

    administracao = recuperar_administracao_ano()
    return render(request,
                  'innapp/rel-ano.html',
                  {'template': relatorio_template(AnoTable(converte_para_map(administracao)),
                                                  year,
                                                  'aluguel_tbl',
                                                  'dt_recebimento',
                                                  'administracao',
                                                  'administração')})


@login_required(login_url='/acesso/login')
def ir_pf_mes_ano(request, year=None):
    if year is None:
        year = datetime.date.today().year

    ir_pf = recuperar_ir_pf_mes_ano(year)
    return render(request,
                  'innapp/rel-mes-ano.html',
                  {'template': relatorio_template(MesAnoTable(converte_para_map(ir_pf)),
                                                  year,
                                                  'aluguel_tbl',
                                                  'dt_recebimento',
                                                  'irpf',
                                                  'IR PF')})


@login_required(login_url='/acesso/login')
def ir_pf_ano(request, year=None):
    if year is None:
        year = datetime.date.today().year

    ir_pf = recuperar_ir_pf_ano()
    return render(request,
                  'innapp/rel-ano.html',
                  {'template': relatorio_template(AnoTable(converte_para_map(ir_pf)),
                                                  year,
                                                  'aluguel_tbl',
                                                  'dt_recebimento',
                                                  'irpf',
                                                  'IR PF')})


@login_required(login_url='/acesso/login')
def relacao_reformas_imoveis(request, year=None):
    if year is None:
        year = datetime.date.today().year

    relacao = reformas_por_imovel(year)
    return render(request,
                  'innapp/rel-mes-ano.html',
                  {'template': relatorio_template(ReformaImovelTable(converte_para_map(relacao, rotulo='endereco')),
                                                  year,
                                                  'aluguel_tbl',
                                                  'dt_recebimento',
                                                  'refimovel',
                                                  'reformas por imóvel')})


@login_required(login_url='/acesso/login')
def relacao_alugueis_pendentes(request, year=None, month=None):
    if year is None:
        year = datetime.date.today().year
    if month is None:
        month = datetime.date.today().month

    pendentes = alugueis_pendentes(mes=month, ano=year)

    current_year = datetime.date.today().year
    available_years = recuperar_anos_disponiveis('aluguel_tbl', 'dt_recebimento')

    # Verifica se o ano atual esta presente na lista, caso contrario, adiciona
    if int(current_year) not in available_years:
        available_years.insert(0, int(current_year))

    template = {
        'all': PendenteTable([{'vencimento': vencimento, 'endereco': endereco} for vencimento, endereco in pendentes]),
        'available_years': available_years,
        'selected_year': year,
        'available_months': range(1, 13),
        'selected_month': month,
        'type_reg': 'pendente',
        'type_reg_pl': 'aluguéis pendentes'
    }

    return render(request, 'innapp/rel-pendentes.html', {'template': template})


@login_required(login_url='/acesso/login')
def relacao_alugueis_pendentes_ano(request, year=None):
    if year is None:
        year = datetime.date.today().year

    alugueis_ano = alugueis_recebidos_ano(year)
    imoveis = {(imovel_id, desc_endereco) for imovel_id, desc_endereco, _ in alugueis_ano}

    IMOVEL_ID_INDEX = 0
    MES_REFERENCIA_INDEX = 2
    relacao = {}
    for imovel_id, desc_endereco in imoveis:
        relacao[desc_endereco] = []
        alugueis_mes_referencia = [al[MES_REFERENCIA_INDEX] for al in alugueis_ano if al[IMOVEL_ID_INDEX] == imovel_id]
        for mes in range(1, 13):
            if mes not in alugueis_mes_referencia:
                relacao[desc_endereco].append(mes)

    # Ordena e transforma em dict novamente
    relacao = dict(OrderedDict(sorted(relacao.items())))
    relacao_datatable = PendenteAnoTable(
        [{'endereco': key, 'meses': relacao[key]} for key in relacao if len(relacao[key]) > 0]
    )

    return render(request,
                  'innapp/rel-mes-ano.html',
                  {'template': relatorio_template(relacao_datatable,
                                                  year,
                                                  'aluguel_tbl',
                                                  'dt_recebimento',
                                                  'pendano',
                                                  'aluguéis pendentes ano')})


@login_required(login_url='/acesso/login')
def aluguel_por_imovel(request, year=None):
    if year is None:
        year = datetime.date.today().year

    relacao = alugueis_por_imovel(year)
    return render(request,
                  'innapp/rel-mes-ano.html',
                  {'template': relatorio_template(AluguelImovelTable(converte_para_map(relacao, rotulo='endereco')),
                                                  year,
                                                  'aluguel_tbl',
                                                  'dt_recebimento',
                                                  'alugimovel',
                                                  'aluguéis por imóvel')})


@login_required(login_url='/acesso/login')
def aluguel_por_mes_referencia(request, year=None, month=None):
    if year is None:
        year = datetime.date.today().year
    if month is None:
        month = datetime.date.today().month

    total_mes = alugueis_mes_referencia(mes=month, ano=year)
    total_a_declarar = alugueis_mes_referencia(mes=month, ano=year, condicao='declarar')
    total_n_declarar = alugueis_mes_referencia(mes=month, ano=year, condicao='nao-declarar')
    totais = [
        {'rotulo': 'total no mês', 'valor': converte_para_numerico(total_mes)},
        {'rotulo': 'total a declarar', 'valor': converte_para_numerico(total_a_declarar)},
        {'rotulo': 'total a não declarar', 'valor': converte_para_numerico(total_n_declarar)},
    ]

    current_year = datetime.date.today().year
    available_years = recuperar_anos_disponiveis('aluguel_tbl', 'dt_recebimento')

    # Verifica se o ano atual esta presente na lista, caso contrario, adiciona
    if int(current_year) not in available_years:
        available_years.insert(0, int(current_year))

    template = {
        'all': TotalTable(totais),
        'available_years': available_years,
        'selected_year': year,
        'available_months': range(1, 13),
        'selected_month': month,
        'type_reg': 'total',
        'type_reg_pl': 'totais'
    }

    return render(request, 'innapp/rel-totais.html', {'template': template})


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


def converte_para_map(registros, rotulo='periodo'):
    return [{rotulo: descricao, 'valor': valor} for descricao, valor in registros]


def converte_para_numerico(data):
    valor = str(data[0][0])
    if valor == 'None':
        return 0.00
    return valor
