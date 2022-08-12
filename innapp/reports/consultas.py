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