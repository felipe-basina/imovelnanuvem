import itertools

from django.db import connection


def recuperar_aluguel_mes_ano(ano):
    cursor = connection.cursor()
    consulta = ('SELECT concat(lpad(cast(extract(month from dt_recebimento) as text), 2, \'0\'), \'/\', extract(year from dt_recebimento)), sum(num_aluguel) '
                'FROM aluguel_tbl '
                'WHERE dt_recebimento <= now() '
                'AND extract(year from dt_recebimento) = %s '
                'group by concat(lpad(cast(extract(month from dt_recebimento) as text), 2, \'0\'), \'/\', extract(year from dt_recebimento)) '
                'order by concat(lpad(cast(extract(month from dt_recebimento) as text), 2, \'0\'), \'/\', extract(year from dt_recebimento)) desc ')
    cursor.execute(consulta, [ano])
    return cursor.fetchall()


def recuperar_aluguel_ano():
    cursor = connection.cursor()
    consulta = ('SELECT cast(extract(year from dt_recebimento) as bigint), sum(num_aluguel) '
                'FROM aluguel_tbl '
                'WHERE dt_recebimento <= now() '
                'group by extract(year from dt_recebimento) '
                'order by extract(year from dt_recebimento) desc ')
    cursor.execute(consulta)
    return cursor.fetchall()


def recuperar_reforma_mes_ano(ano):
    cursor = connection.cursor()
    consulta = ('SELECT concat(lpad(cast(extract(month from dt_reforma) as text), 2, \'0\'), \'/\', extract(year from dt_reforma)), sum(num_reforma) '
                'FROM reforma_tbl '
                'WHERE dt_reforma <= now() '
                'AND extract(year from dt_reforma) = %s '
                'group by concat(lpad(cast(extract(month from dt_reforma) as text), 2, \'0\'), \'/\', extract(year from dt_reforma)) '
                'order by concat(lpad(cast(extract(month from dt_reforma) as text), 2, \'0\'), \'/\', extract(year from dt_reforma)) desc ')
    cursor.execute(consulta, [ano])
    return cursor.fetchall()


def recuperar_reforma_ano():
    cursor = connection.cursor()
    consulta = ('SELECT cast(extract(year from dt_reforma) as bigint), sum(num_reforma) '
                'FROM reforma_tbl '
                'WHERE dt_reforma <= now() '
                'group by extract(year from dt_reforma) '
                'order by extract(year from dt_reforma) desc ')
    cursor.execute(consulta)
    return cursor.fetchall()