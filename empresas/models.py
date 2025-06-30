from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Empresa(TenantMixin):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20, unique=True)
    data_criacao = models.DateField(auto_now_add=True)
    pago_ate = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Dominio(DomainMixin):
    pass  # já possui os campos `domain`, `tenant` e `is_primary`