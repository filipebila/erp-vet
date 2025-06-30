from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

class Client(TenantMixin):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20)
    data_criacao = models.DateField(auto_now_add=True)
    pago_ate = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Domain(DomainMixin):
    pass  # já herda os campos: domain, tenant, is_primary