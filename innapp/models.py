# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django import forms


class ImovelTbl(models.Model):
    idt_imovel = models.BigAutoField(primary_key=True)
    desc_endereco = models.CharField(max_length=400)
    desc_status = models.CharField(max_length=20)
    dt_criacao = models.DateTimeField(default=timezone.now)
    dt_atualizacao = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'imovel_tbl'
        verbose_name = ('Imóveis')

    def __str__(self):
        return self.desc_endereco

    # Permite com que esse campo receba caracteres especiais
    def __unicode__(self):
        return self.desc_endereco


class ImovelForm(ModelForm):
    class Meta:
        model = ImovelTbl
        fields = ['desc_endereco']
        labels = {
            'desc_endereco': 'Endereço imóvel',
        }
        widgets = {
            'desc_endereco': forms.TextInput(attrs={'class': 'form-control', }),
        }

    def __init__(self, *args, **kwargs):
        super(ImovelForm, self).__init__(*args, **kwargs)


class InquilinoTbl(models.Model):
    idt_inquilino = models.BigAutoField(primary_key=True)
    desc_nome = models.CharField(max_length=50)
    desc_tipo = models.CharField(max_length=4)
    desc_status = models.CharField(max_length=20)
    dt_inicio = models.DateField()
    dt_fim = models.DateField()
    num_vencimento = models.IntegerField(default=1)
    dt_criacao = models.DateTimeField(default=timezone.now)
    dt_atualizacao = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'inquilino_tbl'
        verbose_name = ('Inquilino')

    def __str__(self):
        return self.desc_nome

    # Permite com que esse campo receba caracteres especiais
    def __unicode__(self):
        return self.desc_nome


TIPO_PESSOA_OPCOES = (
    ('PF', 'física'),
    ('PJ', 'jurídica')
)

DIAS_OPCOES = [(str(i), str(i)) for i in range(1, 32)]


class InquilinoForm(ModelForm):
    class Meta:
        model = InquilinoTbl
        fields = ['desc_nome', 'desc_tipo', 'dt_inicio', 'dt_fim', 'num_vencimento']
        labels = {
            'desc_nome': 'Inquilino',
            'desc_tipo': 'Tipo',
            'dt_inicio': 'Data início',
            'dt_fim': 'Data fim',
            'num_vencimento': 'Dia vencimento',
        }
        widgets = {
            'desc_nome': forms.TextInput(attrs={'class': 'form-control', }),
            'desc_tipo': forms.RadioSelect(choices=TIPO_PESSOA_OPCOES, attrs={'class': 'form-control', }),
            'dt_inicio': forms.DateInput(format='%d/%m/%Y',
                                         attrs={'class': 'form-control', 'type': 'date',
                                                'placeholder': 'Selecione uma data'}),
            'dt_fim': forms.DateInput(format=('%d/%m/%Y'),
                                      attrs={'class': 'form-control', 'type': 'date',
                                             'placeholder': 'Selecione uma data'}),
            'num_vencimento': forms.Select(choices=DIAS_OPCOES, attrs={'class': 'form-control tamanho_caixa', }),
        }

    def __init__(self, *args, **kwargs):
        super(InquilinoForm, self).__init__(*args, **kwargs)


class AluguelTbl(models.Model):
    idt_aluguel = models.BigAutoField(primary_key=True)
    num_aluguel = models.DecimalField(max_digits=1000, decimal_places=2)
    num_administracao = models.DecimalField(max_digits=1000, decimal_places=2)
    num_acordo = models.DecimalField(max_digits=1000, decimal_places=2)
    dt_recebimento = models.DateField()
    dt_criacao = models.DateTimeField(default=timezone.now)
    dt_atualizacao = models.DateTimeField(default=timezone.now)
    idt_imovel = models.ForeignKey('ImovelTbl', models.DO_NOTHING, db_column='idt_imovel', blank=True, null=True)
    idt_inquilino = models.ForeignKey(
        'InquilinoTbl', models.DO_NOTHING, db_column='idt_inquilino', blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = 'aluguel_tbl'
        verbose_name = ('Aluguel')


class AluguelForm(ModelForm):
    class Meta:
        model = AluguelTbl
        fields = ['idt_imovel', 'idt_inquilino', 'dt_recebimento', 'num_aluguel', 'num_administracao', 'num_acordo']
        labels = {
            'idt_imovel': 'Imóvel',
            'idt_inquilino': 'Inquilino',
            'dt_recebimento': 'Data recebimento',
            'num_aluguel': 'Valor aluguel',
            'num_administracao': 'Valor administração',
            'num_acordo': 'Valor acordo',
        }
        widgets = {
            'idt_imovel': forms.Select(attrs={'class': 'form-control', }),
            'idt_inquilino': forms.Select(attrs={'class': 'form-control', }),
            'dt_recebimento': forms.DateInput(format='%d/%m/%Y',
                                              attrs={'class': 'form-control', 'type': 'date',
                                                     'placeholder': 'Selecione uma data'}),
            'num_aluguel': forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}),
            'num_administracao': forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}),
            'num_acordo': forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super(AluguelForm, self).__init__(*args, **kwargs)


class ReformaTbl(models.Model):
    idt_reforma = models.BigAutoField(primary_key=True)
    num_reforma = models.DecimalField(max_digits=1000, decimal_places=2)
    desc_reforma = models.CharField(max_length=1000)
    dt_reforma = models.DateField()
    dt_criacao = models.DateTimeField(default=timezone.now)
    dt_atualizacao = models.DateTimeField(default=timezone.now)
    idt_imovel = models.ForeignKey('ImovelTbl', models.DO_NOTHING, db_column='idt_imovel', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'reforma_tbl'
        verbose_name = ('Reforma')

    # Permite com que esse campo receba caracteres especiais
    def __unicode__(self):
        return self.desc_reforma


class ReformaForm(ModelForm):
    class Meta:
        model = ReformaTbl
        fields = ['idt_imovel', 'dt_reforma', 'num_reforma', 'desc_reforma']
        labels = {
            'idt_imovel': 'Imóvel',
            'dt_reforma': 'Data reforma',
            'num_reforma': 'Valor reforma',
            'desc_reforma': 'Descrição',
        }
        widgets = {
            'idt_imovel': forms.Select(attrs={'class': 'form-control', }),
            'dt_reforma': forms.DateInput(format='%d/%m/%Y',
                                          attrs={'class': 'form-control', 'type': 'date',
                                                 'placeholder': 'Selecione uma data'}),
            'num_reforma': forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}),
            'desc_reforma': forms.TextInput(attrs={'class': 'form-control', }),
        }

    def __init__(self, *args, **kwargs):
        super(ReformaForm, self).__init__(*args, **kwargs)
