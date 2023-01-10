import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import utc

from .imovel import recuperar_imoveis
from .inquilino import recuperar_inquilinos
from ..models import AluguelTbl, AluguelForm
from ..tables import AluguelTable
from ..utils.utilidades import ajusta_para_apresentacao, recuperar_anos_disponiveis


@login_required(login_url='/acesso/login')
def aluguel_todos(request):
    return render(request, 'innapp/aluguel.html', {'template': aluguel_template()})


@login_required(login_url='/acesso/login')
def aluguel_todos_por_ano(request, year):
    aluguel_map = aluguel_template(idt_reg=0, ano=year)
    aluguel_map['message'] = ('Exibindo aluguéis para o ano de %s' % year)
    aluguel_map['status'] = 'success'
    return render(request, 'innapp/aluguel.html', {'template': aluguel_map})


@login_required(login_url='/acesso/login')
def aluguel_novo(request):
    if request.method == "POST":
        form = AluguelForm(request.POST)
        aluguel = form.save(commit=False)
        aluguel.dt_criacao = datetime.datetime.utcnow().replace(tzinfo=utc)
        aluguel.dt_atualizacao = datetime.datetime.utcnow().replace(tzinfo=utc)
        aluguel.save()

    aluguel_map = aluguel_template()
    aluguel_map['message'] = 'Aluguel salvo com sucesso'
    aluguel_map['status'] = 'success'

    return render(request, 'innapp/aluguel.html', {'template': aluguel_map})


@login_required(login_url='/acesso/login')
def aluguel_por_id(request, idt):
    aluguel_map = {}

    if not idt:
        aluguel_map['message'] = 'Registro inválido'
        aluguel_map['status'] = 'danger'
        return render(request, 'innapp/aluguel.html', {'template': aluguel_map})

    try:
        aluguel = AluguelTbl.objects.get(idt_aluguel=idt)

        dt_recebimento = ajusta_para_apresentacao(aluguel.dt_recebimento)

        aluguel_map = aluguel_template(idt_reg=idt, ano=aluguel.dt_recebimento.year)

        aluguel_form = AluguelForm(initial={
            'idt_imovel': aluguel.idt_imovel,
            'idt_inquilino': aluguel.idt_inquilino,
            'dt_recebimento': dt_recebimento,
            'num_aluguel': aluguel.num_aluguel,
            'mes_referencia': aluguel.mes_referencia,
            'num_administracao': aluguel.num_administracao,
            'num_acordo': aluguel.num_acordo,
        })
        aluguel_map['form'] = aluguel_form
    except AluguelTbl.DoesNotExist:
        aluguel_map['message'] = 'Registro não encontrado'
        aluguel_map['status'] = 'danger'

    return render(request, 'innapp/aluguel.html', {'template': aluguel_dependencias(aluguel_map)})


@login_required(login_url='/acesso/login')
def aluguel_edita(request, idt):
    aluguel_map = {}

    if not idt:
        aluguel_map['message'] = 'Registro inválido'
        aluguel_map['status'] = 'danger'
        return render(request, 'innapp/aluguel.html', {'template': aluguel_map})

    try:
        aluguel_db = AluguelTbl.objects.get(idt_aluguel=idt)
        form = AluguelForm(request.POST)
        aluguel = form.save(commit=False)
        aluguel_atualizado = AluguelTbl(
            idt_aluguel=idt,
            idt_imovel=aluguel.idt_imovel,
            idt_inquilino=aluguel.idt_inquilino,
            dt_recebimento=aluguel.dt_recebimento,
            mes_referencia=aluguel.mes_referencia,
            num_aluguel=aluguel.num_aluguel,
            num_administracao=aluguel.num_administracao,
            num_acordo=aluguel.num_acordo,
            dt_criacao=aluguel_db.dt_criacao,
            dt_atualizacao=datetime.datetime.utcnow().replace(tzinfo=utc),
        )
        aluguel_atualizado.save(force_insert=False)

        aluguel_map = aluguel_template(idt_reg=0, ano=aluguel.dt_recebimento.year)
        aluguel_map['message'] = 'Aluguel atualizado com sucesso'
        aluguel_map['status'] = 'success'
    except AluguelTbl.DoesNotExist:
        aluguel_map['message'] = 'Registro não encontrado'
        aluguel_map['status'] = 'danger'

    return render(request, 'innapp/aluguel.html', {'template': aluguel_map})


def aluguel_template(idt_reg=0, ano=None):
    if ano is None:
        ano = datetime.date.today().year
    all = AluguelTbl.objects.filter(dt_recebimento__year=ano).order_by('-dt_recebimento', '-idt_aluguel')

    current_year = datetime.date.today().year
    available_years = recuperar_anos_disponiveis('aluguel_tbl', 'dt_recebimento')

    # Verifica se o ano atual esta presente na lista, caso contrario, adiciona
    if int(current_year) not in available_years:
        available_years.insert(0, int(current_year))

    aluguel_map = {
        'all': AluguelTable(all),
        'form': AluguelForm(initial={
            'mes_referencia': datetime.date.today().month
        }),
        'idt_reg': idt_reg,
        'available_years': available_years,
        'selected_year': ano
    }

    return aluguel_dependencias(aluguel_map)


def aluguel_dependencias(aluguel_form):
    aluguel_form['form'].fields['idt_imovel'].queryset = recuperar_imoveis()
    aluguel_form['form'].fields['idt_inquilino'].queryset = recuperar_inquilinos()
    return aluguel_form
