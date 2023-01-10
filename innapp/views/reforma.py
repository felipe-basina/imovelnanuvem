import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import utc

from .imovel import recuperar_imoveis
from ..models import ReformaTbl, ReformaForm
from ..tables import ReformaTable
from ..utils.utilidades import recuperar_anos_disponiveis, ajusta_para_apresentacao


@login_required(login_url='/acesso/login')
def reforma_todos(request):
    return render(request, 'innapp/reforma.html', {'template': reforma_template()})


@login_required(login_url='/acesso/login')
def reforma_todos_por_ano(request, year):
    reforma_map = reforma_template(idt_reg=0, ano=year)
    reforma_map['message'] = ('Exibindo reformas para o ano de %s' % year)
    reforma_map['status'] = 'success'
    return render(request, 'innapp/reforma.html', {'template': reforma_map})


@login_required(login_url='/acesso/login')
def reforma_novo(request):
    if request.method == "POST":
        form = ReformaForm(request.POST)
        reforma = form.save(commit=False)
        reforma.dt_criacao = datetime.datetime.utcnow().replace(tzinfo=utc)
        reforma.dt_atualizacao = datetime.datetime.utcnow().replace(tzinfo=utc)
        reforma.save()

    reforma_map = reforma_template()
    reforma_map['message'] = 'Reforma salva com sucesso'
    reforma_map['status'] = 'success'

    return render(request, 'innapp/reforma.html', {'template': reforma_map})


@login_required(login_url='/acesso/login')
def reforma_por_id(request, idt):
    reforma_map = {}

    if not idt:
        reforma_map['message'] = 'Registro inválido'
        reforma_map['status'] = 'danger'
        return render(request, 'innapp/reforma.html', {'template': reforma_map})

    try:
        reforma = ReformaTbl.objects.get(idt_reforma=idt)

        dt_reforma = ajusta_para_apresentacao(reforma.dt_reforma)

        reforma_map = reforma_template(idt_reg=idt, ano=reforma.dt_reforma.year)

        reforma_form = ReformaForm(initial={
            'idt_imovel': reforma.idt_imovel,
            'dt_reforma': dt_reforma,
            'num_reforma': reforma.num_reforma,
            'desc_reforma': reforma.desc_reforma,
        })
        reforma_map['form'] = reforma_form
    except ReformaTbl.DoesNotExist:
        reforma_map['message'] = 'Registro não encontrado'
        reforma_map['status'] = 'danger'

    return render(request, 'innapp/reforma.html', {'template': reforma_dependencias(reforma_map)})


@login_required(login_url='/acesso/login')
def reforma_edita(request, idt):
    reforma_map = {}

    if not idt:
        reforma_map['message'] = 'Registro inválido'
        reforma_map['status'] = 'danger'
        return render(request, 'innapp/reforma.html', {'template': reforma_map})

    try:
        reforma_db = ReformaTbl.objects.get(idt_reforma=idt)
        form = ReformaForm(request.POST)
        reforma = form.save(commit=False)

        reforma_atualizada = ReformaTbl(
            idt_reforma=idt,
            idt_imovel=reforma.idt_imovel,
            dt_reforma=reforma.dt_reforma,
            num_reforma=reforma.num_reforma,
            desc_reforma=reforma.desc_reforma,
            dt_criacao=reforma_db.dt_criacao,
            dt_atualizacao=datetime.datetime.utcnow().replace(tzinfo=utc),
        )
        reforma_atualizada.save(force_insert=False)

        reforma_map = reforma_template(idt_reg=0, ano=reforma.dt_reforma.year)
        reforma_map['message'] = 'Reforma atualizada com sucesso'
        reforma_map['status'] = 'success'
    except ReformaTbl.DoesNotExist:
        reforma_map['message'] = 'Registro não encontrado'
        reforma_map['status'] = 'danger'

    return render(request, 'innapp/reforma.html', {'template': reforma_dependencias(reforma_map)})


def reforma_template(idt_reg=0, ano=None):
    if ano is None:
        ano = datetime.date.today().year
    all = ReformaTbl.objects.filter(dt_reforma__year=ano).order_by('-dt_reforma', '-idt_imovel')

    current_year = datetime.date.today().year
    available_years = recuperar_anos_disponiveis('reforma_tbl', 'dt_reforma')

    # Verifica se o ano atual esta presente na lista, caso contrario, adiciona
    if int(current_year) not in available_years:
        available_years.insert(0, int(current_year))

    reforma_map = {
        'all': ReformaTable(all),
        'form': ReformaForm(),
        'idt_reg': idt_reg,
        'available_years': available_years,
        'selected_year': ano
    }

    return reforma_dependencias(reforma_map)


def reforma_dependencias(reforma_form):
    reforma_form['form'].fields['idt_imovel'].queryset = recuperar_imoveis()
    return reforma_form
