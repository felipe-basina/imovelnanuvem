import datetime

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


def alugueis_pendentes(mes, ano=datetime.date.today().year):
    cursor = connection.cursor()
    consulta = 'SELECT max(it.num_vencimento) as vencimento, im.desc_endereco FROM imovel_tbl im ' \
               'INNER JOIN aluguel_tbl a on im.idt_imovel = a.idt_imovel  ' \
               'INNER JOIN inquilino_tbl it on a.idt_inquilino = it.idt_inquilino ' \
               'WHERE im.desc_endereco in ( ' \
               ' SELECT desc_endereco FROM imovel_tbl ' \
               ' WHERE desc_endereco NOT IN ( ' \
               '    SELECT IM.DESC_ENDERECO FROM ALUGUEL_TBL AL ' \
               '    INNER JOIN IMOVEL_TBL IM ON IM.IDT_IMOVEL = AL.IDT_IMOVEL ' \
               '    WHERE EXTRACT(MONTH FROM DT_RECEBIMENTO) = %s ' \
               '    AND EXTRACT(YEAR FROM DT_RECEBIMENTO) = %s ' \
               '    ORDER BY AL.DT_RECEBIMENTO DESC, IM.desc_endereco ' \
               '    ) ' \
               '    AND desc_status = \'ATIVO\' ' \
               ') ' \
               'GROUP BY im.desc_endereco ' \
               'ORDER BY vencimento, im.desc_endereco '
    cursor.execute(consulta, [mes, ano])
    return cursor.fetchall()


def reformas_por_imovel(ano=datetime.date.today().year):
    cursor = connection.cursor()
    consulta = 'SELECT im.desc_endereco, sum(num_reforma) AS total ' \
               'FROM reforma_tbl ref ' \
               'INNER JOIN imovel_tbl im ON ref.idt_imovel = im.idt_imovel ' \
               'WHERE EXTRACT(year from dt_reforma) = %s ' \
               'GROUP BY im.desc_endereco, EXTRACT(year from dt_reforma) ' \
               'ORDER BY im.desc_endereco '
    cursor.execute(consulta, [ano])
    return cursor.fetchall()


def alugueis_por_imovel(ano):
    cursor = connection.cursor()
    consulta = 'SELECT it.desc_endereco, sum(al.num_aluguel) AS total FROM aluguel_tbl al ' \
               'INNER JOIN imovel_tbl it on al.idt_imovel = it.idt_imovel ' \
               'WHERE EXTRACT(YEAR FROM al.dt_recebimento) = %s ' \
               'GROUP BY it.desc_endereco ' \
               'ORDER BY it.desc_endereco '
    cursor.execute(consulta, [ano])
    return cursor.fetchall()
