# Create your models here. - core/models.py

from django.db import models

class Tutor(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    endereco = models.TextField(blank=True)
    observacoes = models.TextField(blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Paciente(models.Model):
    ESPECIE_CHOICES = [
        ('Cachorro', 'Cachorro'),
        ('Gato', 'Gato'),
    ]

    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Fêmea', 'Fêmea'),
    ]

    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='pacientes')
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    raca = models.CharField(max_length=50)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    data_nascimento = models.DateField(null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    microchip = models.CharField(max_length=30, blank=True)
    alergias = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome} ({self.especie})"


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('Confirmado', 'Confirmado'),
        ('Pendente', 'Pendente'),
        ('Cancelado', 'Cancelado')
    ]

    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='agendamentos')
    data_hora = models.DateTimeField(null=True, blank=True)
    motivo = models.CharField(max_length=200)
    observacoes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmado')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.data_hora:
            return f'{self.paciente.nome} - {self.data_hora.strftime("%d/%m/%Y %H:%M")}'
        return f'{self.paciente.nome} - Pendente'
    
class Consulta(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='consultas')
    agendamento = models.OneToOneField('Agendamento', on_delete=models.CASCADE, related_name='consulta', null=True, blank=True)
    data_hora = models.DateTimeField()

    motivo = models.CharField(max_length=200)  # queixa principal
    anamnese = models.TextField(blank=True)    # novo campo
    exame_fisico = models.TextField(blank=True)  # novo campo
    diagnostico = models.TextField(blank=True)   # novo campo
    exames_solicitados = models.TextField(blank=True)  # substitui "prescrição"
    tratamento = models.TextField(blank=True)  # orientações/medicamentos
    observacoes = models.TextField(blank=True)  # usado para transcrição por voz

    retorno_necessario = models.BooleanField(default=False)
    data_retorno = models.DateTimeField(null=True, blank=True)
    analise_ia = models.TextField(blank=True, null=True)
    status_analise_ia = models.CharField(
        max_length=20,
        choices=[
            ("pendente", "Pendente"),
            ("em_analise", "Em Análise"),
            ("concluida", "Concluída"),
            ("erro", "Erro"),
        ],
        default="pendente"
    )

    class Meta:
        ordering = ['-data_hora']

    def __str__(self):
        return f"{self.paciente.nome} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
    
class ArquivoConsulta(models.Model):
    TIPO_ARQUIVO = [
        ('foto', 'Foto'),
        ('video', 'Vídeo'),
    ]

    consulta = models.ForeignKey('Consulta', on_delete=models.CASCADE, related_name='arquivos')
    arquivo = models.FileField(upload_to='consultas/arquivos/')
    tipo = models.CharField(max_length=10, choices=TIPO_ARQUIVO)
    tamanho_mb = models.FloatField(help_text="Tamanho do arquivo em MB")
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.arquivo:
            self.tamanho_mb = round(self.arquivo.size / (1024 * 1024), 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo.capitalize()} - {self.consulta} - {self.tamanho_mb}MB"