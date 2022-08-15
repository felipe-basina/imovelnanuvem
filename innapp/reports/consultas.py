import itertools

from django.db import connection


def recuperar_aluguel_mes_ano(ano):
    cursor = connection.cursor()
    consulta = consulta_mes_ano('aluguel_tbl', 'dt_recebimento', 'num_aluguel')
    cursor.execute(consulta, [ano])
    return cursor.fetchall()


def recuperar_aluguel_ano():
    cursor = connection.cursor()
    consulta = consulta_ano('aluguel_tbl', 'dt_recebimento', 'num_aluguel')
    cursor.execute(consulta)
    return cursor.fetchall()


def recuperar_reforma_mes_ano(ano):
    cursor = connection.cursor()
    consulta = consulta_mes_ano('reforma_tbl', 'dt_reforma', 'num_reforma')
    cursor.execute(consulta, [ano])
    return cursor.fetchall()


def recuperar_reforma_ano():
    cursor = connection.cursor()
    consulta = consulta_ano('reforma_tbl', 'dt_reforma', 'num_reforma')
    cursor.execute(consulta)
    return cursor.fetchall()


def recuperar_administracao_mes_ano(ano):
    cursor = connection.cursor()
    consulta = consulta_mes_ano('aluguel_tbl', 'dt_recebimento', 'num_administracao')
    cursor.execute(consulta, [ano])
    return cursor.fetchall()


def recuperar_administracao_ano():
    cursor = connection.cursor()
    consulta = consulta_ano('aluguel_tbl', 'dt_recebimento', 'num_administracao')
    cursor.execute(consulta)
    return cursor.fetchall()


def recuperar_ir_pf_mes_ano(ano):
    cursor = connection.cursor()
    consulta = consulta_mes_ano('aluguel_tbl', 'dt_recebimento', 'num_aluguel', inner_join=True)
    cursor.execute(consulta, [ano])
    return cursor.fetchall()


def recuperar_ir_pf_ano():
    cursor = connection.cursor()
    consulta = consulta_ano('aluguel_tbl', 'dt_recebimento', 'num_aluguel', inner_join=True)
    cursor.execute(consulta)
    return cursor.fetchall()


def consulta_mes_ano(tabela, coluna_data, coluna_valor, inner_join=False):
    return (
        'SELECT concat(lpad(cast(extract(month from _coluna_data_) as text), 2, \'0\'), \'/\', extract(year from _coluna_data_)), sum(_coluna_valor_) '
        'FROM _tabela_ _inner_join_ '
        'WHERE _coluna_data_ <= now() '
        'AND extract(year from _coluna_data_) = %s '
        'group by concat(lpad(cast(extract(month from _coluna_data_) as text), 2, \'0\'), \'/\', extract(year from _coluna_data_)) '
        'order by concat(lpad(cast(extract(month from _coluna_data_) as text), 2, \'0\'), \'/\', extract(year from _coluna_data_)) desc '
        .replace('_inner_join_', inquilino_inner_join_clause() if inner_join else '')
        .replace('_coluna_data_', coluna_data)
        .replace('_coluna_valor_', coluna_valor)
        .replace('_tabela_', tabela)
    )


def consulta_ano(tabela, coluna_data, coluna_valor, inner_join=False):
    return (
        'SELECT cast(extract(year from _coluna_data_) as bigint), sum(_coluna_valor_) '
        'FROM _tabela_ _inner_join_ '
        'WHERE _coluna_data_ <= now() '
        'group by extract(year from _coluna_data_) '
        'order by extract(year from _coluna_data_) desc '
        .replace('_inner_join_', inquilino_inner_join_clause() if inner_join else '')
        .replace('_coluna_data_', coluna_data)
        .replace('_coluna_valor_', coluna_valor)
        .replace('_tabela_', tabela)
    )


def inquilino_inner_join_clause():
    return ' INNER JOIN inquilino_tbl inq ON _tabela_.idt_inquilino = inq.idt_inquilino and inq.desc_tipo = \'PF\' '
