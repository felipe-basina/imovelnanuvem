# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


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
        return "{0} | {1}".format(self.desc_endereco, self.desc_status)

    # Permite com que esse campo receba caracteres especiais
    def __unicode__(self):
        return self.desc_endereco


class InquilinoTbl(models.Model):
    idt_inquilino = models.BigAutoField(primary_key=True)
    desc_nome = models.CharField(max_length=50)
    desc_tipo = models.CharField(max_length=4)
    desc_status = models.CharField(max_length=20)
    dt_inicio = models.DateField()
    dt_fim = models.DateField()
    dt_vencimento = models.DateField()
    dt_criacao = models.DateTimeField(default=timezone.now)
    dt_atualizacao = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'inquilino_tbl'
        verbose_name = ('Inquilino')

    def __str__(self):
        return "{0} | {1} | {2}".format(self.desc_nome, self.desc_tipo, self.desc_status)

    # Permite com que esse campo receba caracteres especiais
    def __unicode__(self):
        return self.desc_nome


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
