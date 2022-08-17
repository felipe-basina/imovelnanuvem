from table import Table
from table.columns import Column, DatetimeColumn, LinkColumn, Link
from table.utils import A


class ImovelTable(Table):
    desc_endereco = Column(header='endereço', field='desc_endereco')
    dt_criacao = DatetimeColumn(header='dt. criação', field='dt_criacao', format='%d/%m/%Y %H:%M')
    dt_atualizacao = DatetimeColumn(header='dt. atualização', field='dt_atualizacao', format='%d/%m/%Y %H:%M')
    acoes = LinkColumn(header='ações', delimiter=' | ', sortable=False, links=[
        Link(text='editar', viewname='editar_imovel', args=[A('pk')]),
        Link(text='desativar', viewname='desativar_imovel', args=[A('pk')])
    ])


class InquilinoTable(Table):
    desc_nome = Column(header='nome', field='desc_nome')
    desc_tipo = Column(header='tipo', field='desc_tipo')
    num_vencimento = Column(header='dia vencimento', field='num_vencimento')
    dt_inicio = DatetimeColumn(header='dt. início', field='dt_inicio', format='%d/%m/%Y')
    dt_fim = DatetimeColumn(header='dt. fim', field='dt_fim', format='%d/%m/%Y')
    dt_criacao = DatetimeColumn(header='dt. criação', field='dt_criacao', format='%d/%m/%Y %H:%M')
    dt_atualizacao = DatetimeColumn(header='dt. atualização', field='dt_atualizacao', format='%d/%m/%Y %H:%M')
    acoes = LinkColumn(header='ações', delimiter=' | ', sortable=False, links=[
        Link(text='editar', viewname='editar_inquilino', args=[A('pk')]),
        Link(text='desativar', viewname='desativar_inquilino', args=[A('pk')])
    ])


class AluguelTable(Table):
    idt_imovel = Column(header='imóvel', field='idt_imovel')
    idt_inquilino = Column(header='inquilino', field='idt_inquilino')
    dt_recebimento = DatetimeColumn(header='dt. recebimento', field='dt_recebimento', format='%d/%m/%Y')
    num_aluguel = Column(header='aluguel', field='num_aluguel')
    num_administracao = Column(header='administração', field='num_administracao')
    num_acordo = Column(header='acordo', field='num_acordo')
    dt_criacao = DatetimeColumn(header='dt. criação', field='dt_criacao', format='%d/%m/%Y %H:%M')
    dt_atualizacao = DatetimeColumn(header='dt. atualização', field='dt_atualizacao', format='%d/%m/%Y %H:%M')
    acoes = LinkColumn(header='ações', sortable=False, links=[
        Link(text='editar', viewname='editar_aluguel', args=[A('pk')])
    ])


class ReformaTable(Table):
    idt_imovel = Column(header='imóvel', field='idt_imovel')
    dt_reforma = DatetimeColumn(header='dt. reforma', field='dt_reforma', format='%d/%m/%Y')
    num_reforma = Column(header='reforma', field='num_reforma')
    desc_reforma = Column(header='descrição', field='desc_reforma')
    dt_criacao = DatetimeColumn(header='dt. criação', field='dt_criacao', format='%d/%m/%Y %H:%M')
    dt_atualizacao = DatetimeColumn(header='dt. atualização', field='dt_atualizacao', format='%d/%m/%Y %H:%M')
    acoes = LinkColumn(header='ações', sortable=False, links=[
        Link(text='editar', viewname='editar_reforma', args=[A('pk')])
    ])


class MesAnoTable(Table):
    periodo = Column(header='mês/ano', field='periodo')
    valor = Column(header='valor', field='valor')


class AnoTable(Table):
    periodo = Column(header='ano', field='periodo')
    valor = Column(header='valor', field='valor')


class PendenteTable(Table):
    pendente = Column(header='endereço', field='endereco')