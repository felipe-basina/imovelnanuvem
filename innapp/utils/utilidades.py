import itertools

from django.db import connection


def ajusta_para_apresentacao(data):
    dia = data.day
    mes = data.month
    ano = data.year

    dia = completar_parte_registro_data(dia)
    mes = completar_parte_registro_data(mes)

    # Para ser apresentada corretamente na tela, a data precisa estar no formato
    # yyyy-MM-dd
    return str(ano) + '-' + str(mes) + '-' + str(dia)


# Adiciona '0' ao dia ou mes. Exemplo: '1' = '01'
def completar_parte_registro_data(parte_data):
    if len(str(parte_data)) < 2:
        parte_data = '0' + str(parte_data)
    return parte_data


def recuperar_anos_disponiveis(tabela, coluna):
    query = 'SELECT cast(EXTRACT(year FROM {0}) as bigint) as ANOS ' \
            'FROM {1} ' \
            'GROUP BY EXTRACT(year FROM {2}) ' \
            'ORDER BY EXTRACT(year FROM {3}) DESC '\
        .format(coluna, tabela, coluna, coluna)

    cursor = connection.cursor()
    cursor.execute(query)
    lista = cursor.fetchall()
    # Converte a tupla em lista
    return list(itertools.chain.from_iterable(lista))
