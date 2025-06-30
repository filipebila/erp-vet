from django.contrib.auth.models import AbstractUser
from django.db import models
from tenants.models import Client  # Importa o modelo de tenant


class Usuario(AbstractUser):
    cargo = models.CharField(max_length=50, choices=[
        ("recepcao", "Recepção"),
        ("veterinario", "Veterinário"),
        ("auxiliar", "Auxiliar"),
        ("financeiro", "Financeiro"),
        ("gerente", "Gerente"),
        ("admin", "Administrador"),
    ])
    
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username