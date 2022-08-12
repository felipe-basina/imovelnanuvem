from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import utc
import datetime

from ..models import InquilinoTbl, InquilinoForm
from ..utils.utilidades import ajusta_para_apresentacao


@login_required(login_url='/acesso/login')
def inquilino_todos(request):
    return render(request, 'innapp/inquilino.html', {'template': inquilino_template()})


@login_required(login_url='/acesso/login')
def inquilino_novo(request):
    if request.method == "POST":
        form = InquilinoForm(request.POST)
        inquilino = form.save(commit=False)
        inquilino.desc_status = 'ATIVO'
        inquilino.dt_criacao = datetime.datetime.utcnow().replace(tzinfo=utc)
        inquilino.dt_atualizacao = datetime.datetime.utcnow().replace(tzinfo=utc)
        inquilino.save()

    inquilino_map = inquilino_template()
    inquilino_map['message'] = 'Inquilino salvo com sucesso'
    inquilino_map['status'] = 'success'

    return render(request, 'innapp/inquilino.html', {'template': inquilino_map})


@login_required(login_url='/acesso/login')
def inquilino_por_id(request, idt):
    inquilino_map = inquilino_template(idt)

    if not idt:
        inquilino_map['message'] = 'Registro inválido'
        inquilino_map['status'] = 'danger'
        return render(request, 'innapp/inquilino.html', {'template': inquilino_map})

    try:
        inquilino = InquilinoTbl.objects.get(idt_inquilino=idt, desc_status='ATIVO')

        dt_inicio = ajusta_para_apresentacao(inquilino.dt_inicio)
        dt_fim = ajusta_para_apresentacao(inquilino.dt_fim)

        inquilino_form = InquilinoForm(initial={
            'desc_nome': inquilino.desc_nome,
            'desc_tipo': inquilino.desc_tipo,
            'num_vencimento': inquilino.num_vencimento,
            'dt_inicio': dt_inicio,
            'dt_fim': dt_fim,
        })
        inquilino_map['form'] = inquilino_form
    except InquilinoTbl.DoesNotExist:
        inquilino_map['message'] = 'Registro não encontrado'
        inquilino_map['status'] = 'danger'

    return render(request, 'innapp/inquilino.html', {'template': inquilino_map})


@login_required(login_url='/acesso/login')
def inquilino_edita(request, idt):
    inquilino_map = inquilino_template()

    if not idt:
        inquilino_map['message'] = 'Registro inválido'
        inquilino_map['status'] = 'danger'
        return render(request, 'innapp/inquilino.html', {'template': inquilino_map})

    try:
        inquilino_db = InquilinoTbl.objects.get(idt_inquilino=idt, desc_status='ATIVO')
        form = InquilinoForm(request.POST)
        inquilino = form.save(commit=False)
        inquilino_atualizado = InquilinoTbl(
            idt_inquilino=idt,
            desc_nome=inquilino.desc_nome,
            desc_tipo=inquilino.desc_tipo,
            num_vencimento=inquilino.num_vencimento,
            dt_inicio=inquilino.dt_inicio,
            dt_fim=inquilino.dt_fim,
            desc_status=inquilino_db.desc_status,
            dt_criacao=inquilino_db.dt_criacao,
            dt_atualizacao=datetime.datetime.utcnow().replace(tzinfo=utc),
        )
        inquilino_atualizado.save(force_insert=False)

        inquilino_map['message'] = 'Inquilino atualizado com sucesso'
        inquilino_map['status'] = 'success'
    except InquilinoTbl.DoesNotExist:
        inquilino_map['message'] = 'Registro não encontrado'
        inquilino_map['status'] = 'danger'

    return render(request, 'innapp/inquilino.html', {'template': inquilino_map})


@login_required(login_url='/acesso/login')
def inquilino_desativa(request, idt):
    inquilino_map = inquilino_template()

    if not idt:
        inquilino_map['message'] = 'Registro inválido'
        inquilino_map['status'] = 'danger'
        return render(request, 'innapp/inquilino.html', {'template': inquilino_map})

    try:
        inquilino_db = InquilinoTbl.objects.get(idt_inquilino=idt)
        inquilino_atualizado = InquilinoTbl(
            idt_inquilino=idt,
            desc_nome=inquilino_db.desc_nome,
            desc_tipo=inquilino_db.desc_tipo,
            num_vencimento=inquilino_db.num_vencimento,
            dt_inicio=inquilino_db.dt_inicio,
            dt_fim=inquilino_db.dt_fim,
            desc_status='INATIVO',
            dt_criacao=inquilino_db.dt_criacao,
            dt_atualizacao=datetime.datetime.utcnow().replace(tzinfo=utc),
        )
        inquilino_atualizado.save(force_insert=False)

        inquilino_map['message'] = 'Inquilino atualizado com sucesso'
        inquilino_map['status'] = 'success'
    except InquilinoTbl.DoesNotExist:
        inquilino_map['message'] = 'Registro não encontrado'
        inquilino_map['status'] = 'danger'

    return render(request, 'innapp/inquilino.html', {'template': inquilino_map})


def inquilino_template(idt_reg=0):
    inquilino_map = {
        'all': InquilinoTbl.objects.filter(desc_status='ATIVO').order_by('desc_nome'),
        'form': InquilinoForm(),
        'idt_reg': idt_reg
    }
    return inquilino_map


def recuperar_inquilinos(all=False):
    if all == True:
        return InquilinoTbl.objects.all().order_by('desc_nome')
    else:
        return InquilinoTbl.objects.filter(desc_status='ATIVO').order_by('desc_nome')
