from django.http import *
from django.shortcuts import render
from django.utils.timezone import utc
import datetime

from ..models import ImovelTbl, ImovelForm


def imovel_todos(request):
    imovel_map = {
        'all': ImovelTbl.objects.filter(desc_status='ATIVO').order_by('idt_imovel'),
        'form': ImovelForm(),
        'idt_reg': 0
    }
    return render(request, 'innapp/imovel.html', {'template': imovel_map})


def imovel_novo(request):
    if request.method == "POST":
        form = ImovelForm(request.POST)
        imovel = form.save(commit=False)
        imovel.desc_status = 'ATIVO'
        imovel.dt_criacao = datetime.datetime.utcnow().replace(tzinfo=utc)
        imovel.dt_atualizacao = datetime.datetime.utcnow().replace(tzinfo=utc)
        imovel.save()

    imovel_map = {
        'all': ImovelTbl.objects.all().order_by('idt_imovel'),
        'form': ImovelForm(),
        'idt_reg': 0,
        'message': 'Imóvel salvo com sucesso',
        'status': 'success'
    }

    return render(request, 'innapp/imovel.html', {'template': imovel_map})


def imovel_por_id(request, idt):
    imovel_map = {'idt_reg': 0}

    if not idt:
        imovel_map['message'] = 'Registro inválido'
        imovel_map['status'] = 'danger'
        return render(request, 'innapp/imovel.html', {'template': imovel_map})

    try:
        imovel = ImovelTbl.objects.get(idt_imovel=idt)
        imovel_form = ImovelForm(initial={
            'desc_endereco': imovel.desc_endereco
        })

        imovel_map = {
            'all': ImovelTbl.objects.all().order_by('idt_imovel'),
            'form': imovel_form,
            'idt_reg': imovel.idt_imovel
        }
    except ImovelTbl.DoesNotExist:
        imovel_map['message'] = 'Registro não encontrado'
        imovel_map['status'] = 'danger'

    return render(request, 'innapp/imovel.html', {'template': imovel_map})


def imovel_edita(request, idt):
    imovel_map = {'idt_reg': 0}

    if not idt:
        imovel_map['message'] = 'Registro inválido'
        imovel_map['status'] = 'danger'
        return render(request, 'innapp/imovel.html', {'template': imovel_map})

    try:
        imovel_db = ImovelTbl.objects.get(idt_imovel=idt)
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

        imovel_map = {
            'all': ImovelTbl.objects.filter(desc_status='ATIVO').order_by('idt_imovel'),
            'form': ImovelForm(),
            'message': 'Imóvel atualizado com sucesso',
            'status': 'success'
        }
    except ImovelTbl.DoesNotExist:
        imovel_map['message'] = 'Registro não encontrado'
        imovel_map['status'] = 'danger'

    return render(request, 'innapp/imovel.html', {'template': imovel_map})


def imovel_desativa(request, idt):
    imovel_map = {'idt_reg': 0}

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

        imovel_map = {
            'all': ImovelTbl.objects.filter(desc_status='ATIVO').order_by('idt_imovel'),
            'form': ImovelForm(),
            'message': 'Imóvel atualizado com sucesso',
            'status': 'success'
        }
    except ImovelTbl.DoesNotExist:
        imovel_map['message'] = 'Registro não encontrado'
        imovel_map['status'] = 'danger'

    return render(request, 'innapp/imovel.html', {'template': imovel_map})
