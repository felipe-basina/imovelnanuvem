from table import Table
from table.columns import Column, DatetimeColumn, LinkColumn, Link
from table.utils import A


class ImovelTable(Table):
    desc_endereco = Column(header='endereço', field='desc_endereco', header_attrs={'style': 'text-align:center;'})
    dt_criacao = DatetimeColumn(header='dt. criação', field='dt_criacao', format='%d/%m/%Y %H:%M', header_attrs={'style': 'text-align:center;'})
    dt_atualizacao = DatetimeColumn(header='dt. atualização', field='dt_atualizacao', format='%d/%m/%Y %H:%M', header_attrs={'style': 'text-align:center;'})
    acoes = LinkColumn(header='ações', delimiter=' | ', sortable=False, links=[
        Link(text='', viewname='editar_imovel', args=[A('pk')], attrs={'class': 'fa fa-pencil-square-o fa-fw'}),
        Link(text='', viewname='desativar_imovel', args=[A('pk')], attrs={'class': 'fa fa-trash-o fa-fw'})
    ], header_attrs={'style': 'text-align:center;'})


class InquilinoTable(Table):
    desc_nome = Column(header='nome', field='desc_nome', header_attrs={'style': 'text-align:center;'})
    desc_tipo = Column(header='tipo', field='desc_tipo', header_attrs={'style': 'text-align:center;'})
    num_vencimento = Column(header='dia vencimento', field='num_vencimento', header_attrs={'style': 'text-align:center;'})
    dt_inicio = DatetimeColumn(header='dt. início', field='dt_inicio', format='%d/%m/%Y', header_attrs={'style': 'text-align:center;'})
    dt_fim = DatetimeColumn(header='dt. fim', field='dt_fim', format='%d/%m/%Y', header_attrs={'style': 'text-align:center;'})
    dt_criacao = DatetimeColumn(header='dt. criação', field='dt_criacao', format='%d/%m/%Y %H:%M', header_attrs={'style': 'text-align:center;'})
    dt_atualizacao = DatetimeColumn(header='dt. atualização', field='dt_atualizacao', format='%d/%m/%Y %H:%M', header_attrs={'style': 'text-align:center;'})
    acoes = LinkColumn(header='ações', delimiter=' | ', sortable=False, links=[
        Link(text='', viewname='editar_inquilino', args=[A('pk')], attrs={'class': 'fa fa-pencil-square-o fa-fw'}),
        Link(text='', viewname='desativar_inquilino', args=[A('pk')], attrs={'class': 'fa fa-trash-o fa-fw'})
    ], header_attrs={'style': 'text-align:center;'})


class AluguelTable(Table):
    idt_imovel = Column(header='imóvel', field='idt_imovel', header_attrs={'style': 'text-align:center;'})
    idt_inquilino = Column(header='inquilino', field='idt_inquilino', header_attrs={'style': 'text-align:center;'})
    dt_recebimento = DatetimeColumn(header='dt. recebimento', field='dt_recebimento', format='%d/%m/%Y', header_attrs={'style': 'text-align:center;'})
    num_aluguel = Column(header='aluguel', field='num_aluguel', header_attrs={'style': 'text-align:center;'})
    num_administracao = Column(header='administração', field='num_administracao', header_attrs={'style': 'text-align:center;'})
    num_acordo = Column(header='acordo', field='num_acordo', header_attrs={'style': 'text-align:center;'})
    dt_criacao = DatetimeColumn(header='dt. criação', field='dt_criacao', format='%d/%m/%Y %H:%M', header_attrs={'style': 'text-align:center;'})
    dt_atualizacao = DatetimeColumn(header='dt. atualização', field='dt_atualizacao', format='%d/%m/%Y %H:%M', header_attrs={'style': 'text-align:center;'})
    acoes = LinkColumn(header='ações', sortable=False, links=[
        Link(text='', viewname='editar_aluguel', args=[A('pk')], attrs={'class': 'fa fa-pencil-square-o fa-fw'})
    ], header_attrs={'style': 'text-align:center;'})


class ReformaTable(Table):
    idt_imovel = Column(header='imóvel', field='idt_imovel', header_attrs={'style': 'text-align:center;'})
    dt_reforma = DatetimeColumn(header='dt. reforma', field='dt_reforma', format='%d/%m/%Y', header_attrs={'style': 'text-align:center;'})
    num_reforma = Column(header='reforma', field='num_reforma', header_attrs={'style': 'text-align:center;'})
    desc_reforma = Column(header='descrição', field='desc_reforma', header_attrs={'style': 'text-align:center;'})
    dt_criacao = DatetimeColumn(header='dt. criação', field='dt_criacao', format='%d/%m/%Y %H:%M', header_attrs={'style': 'text-align:center;'})
    dt_atualizacao = DatetimeColumn(header='dt. atualização', field='dt_atualizacao', format='%d/%m/%Y %H:%M', header_attrs={'style': 'text-align:center;'})
    acoes = LinkColumn(header='ações', sortable=False, links=[
        Link(text='', viewname='editar_reforma', args=[A('pk')], attrs={'class': 'fa fa-pencil-square-o fa-fw'})
    ], header_attrs={'style': 'text-align:center;'})


class MesAnoTable(Table):
    periodo = Column(header='mês/ano', field='periodo', header_attrs={'style': 'text-align:center;'})
    valor = Column(header='valor', field='valor', header_attrs={'style': 'text-align:center;'})


class AnoTable(Table):
    periodo = Column(header='ano', field='periodo', header_attrs={'style': 'text-align:center;'})
    valor = Column(header='valor', field='valor', header_attrs={'style': 'text-align:center;'})


class PendenteTable(Table):
    pendente = Column(header='imóvel', field='endereco', header_attrs={'style': 'text-align:center;'})


class ReformaImovelTable(Table):
    endereco = Column(header='imóvel', field='endereco', header_attrs={'style': 'text-align:center;'})
    valor = Column(header='valor', field='valor', header_attrs={'style': 'text-align:center;'})