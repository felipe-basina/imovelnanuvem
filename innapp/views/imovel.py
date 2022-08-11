from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import utc
import datetime

from ..models import ImovelTbl, ImovelForm


@login_required(login_url='/acesso/login')
def imovel_todos(request):
    return render(request, 'innapp/imovel.html', {'template': imovel_template()})


@login_required(login_url='/acesso/login')
def imovel_novo(request):
    if request.method == "POST":
        form = ImovelForm(request.POST)
        imovel = form.save(commit=False)
        imovel.desc_status = 'ATIVO'
        imovel.dt_criacao = datetime.datetime.utcnow().replace(tzinfo=utc)
        imovel.dt_atualizacao = datetime.datetime.utcnow().replace(tzinfo=utc)
        imovel.save()

    imovel_map = imovel_template()
    imovel_map['message'] = 'Imóvel salvo com sucesso'
    imovel_map['status'] = 'success'

    return render(request, 'innapp/imovel.html', {'template': imovel_map})


@login_required(login_url='/acesso/login')
def imovel_por_id(request, idt):
    imovel_map = imovel_template(idt)

    if not idt:
        imovel_map['message'] = 'Registro inválido'
        imovel_map['status'] = 'danger'
        return render(request, 'innapp/imovel.html', {'template': imovel_map})

    try:
        imovel = ImovelTbl.objects.get(idt_imovel=idt)
        imovel_form = ImovelForm(initial={
            'desc_endereco': imovel.desc_endereco
        })
        imovel_map['form'] = imovel_form
    except ImovelTbl.DoesNotExist:
        imovel_map['message'] = 'Registro não encontrado'
        imovel_map['status'] = 'danger'

    return render(request, 'innapp/imovel.html', {'template': imovel_map})


@login_required(login_url='/acesso/login')
def imovel_edita(request, idt):
    imovel_map = imovel_template()

    if not idt:
        imovel_map['message'] = 'Registro inválido'
        imovel_map['status'] = 'danger'
        return render(request, 'innapp/imovel.html', {'template': imovel_map})

    try:
        imovel_db = ImovelTbl.objects.get(idt_imovel=idt, desc_status='ATIVO')
        form = ImovelForm(request.POST)
        imovel = form.save(commit=False)
        imovel_atualizado = ImovelTbl(
            idt_imovel=idt,
            desc_status=imovel_db.desc_status,
            desc_endereco=imovel.desc_endereco,
            dt_criacao=imovel_db.dt_criacao,
            dt_atualizacao=datetime.datetime.utcnow().replace(tzinfo=utc),
        )
        imovel_atualizado.save(force_insert=False)

        imovel_map['message'] = 'Imóvel atualizado com sucesso'
        imovel_map['status'] = 'success'
    except ImovelTbl.DoesNotExist:
        imovel_map['message'] = 'Registro não encontrado'
        imovel_map['status'] = 'danger'

    return render(request, 'innapp/imovel.html', {'template': imovel_map})


@login_required(login_url='/acesso/login')
def imovel_desativa(request, idt):
    imovel_map = imovel_template()

    if not idt:
        imovel_map['message'] = 'Registro inválido'
        imovel_map['status'] = 'danger'
        return render(request, 'innapp/imovel.html', {'template': imovel_map})

    try:
        imovel_db = ImovelTbl.objects.get(idt_imovel=idt)
        imovel_atualizado = ImovelTbl(
            idt_imovel=idt,
            desc_status='INATIVO',
            desc_endereco=imovel_db.desc_endereco,
            dt_criacao=imovel_db.dt_criacao,
            dt_atualizacao=datetime.datetime.utcnow().replace(tzinfo=utc),
        )
        imovel_atualizado.save(force_insert=False)

        imovel_map['message'] = 'Imóvel atualizado com sucesso'
        imovel_map['status'] = 'success'
    except ImovelTbl.DoesNotExist:
        imovel_map['message'] = 'Registro não encontrado'
        imovel_map['status'] = 'danger'

    return render(request, 'innapp/imovel.html', {'template': imovel_map})


def imovel_template(idt_reg=0):
    imovel_map = {
        'all': ImovelTbl.objects.filter(desc_status='ATIVO').order_by('idt_imovel'),
        'form': ImovelForm(),
        'idt_reg': idt_reg
    }
    return imovel_map
