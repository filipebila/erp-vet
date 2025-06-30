#core/forms.py

from django import forms
from .models import Paciente, Tutor, Agendamento, Consulta

RACAS_CACHORRO = [
    '--- Selecione uma raça ---',
    'Sem Raça Definida',
    'Outra',
    'Akita',
    'Basset Hound',
    'Beagle',
    'Bernese',
    'Bichon Frisé',
    'Border Collie',
    'Boston Terrier',
    'Boxer',
    'Bulldog Francês',
    'Bulldog Inglês',
    'Cane Corso',
    'Chihuahua',
    'Cocker Spaniel',
    'Dachshund (Salsicha)',
    'Doberman',
    'Fox Paulistinha',
    'Golden Retriever',
    'Husky Siberiano',
    'Jack Russell Terrier',
    'Labrador Retriever',
    'Lhasa Apso',
    'Maltês',
    'Pastor Alemão',
    'Pastor Australiano',
    'Pastor de Shetland',
    'Pinscher',
    'Pit Bull',
    'Pomerânia (Spitz Alemão)',
    'Poodle',
    'Pug',
    'Rottweiler',
    'Schnauzer Miniatura',
    'Shar Pei',
    'Shih Tzu',
    'Staffordshire Bull Terrier',
    'Weimaraner',
    'Whippet',
    'Yorkshire Terrier',
]

RACAS_GATO = [
    '--- Selecione uma raça ---',
    'Sem Raça Definida',
    'Outra',
    'Abissínio',
    'Angorá',
    'Azul Russo',
    'Bengal',
    'Birmanês',
    'British Shorthair',
    'Burguês',
    'Chartreux',
    'Cornish Rex',
    'Exótico',
    'Himalaio',
    'Korat',
    'Maine Coon',
    'Manx',
    'Norueguês da Floresta',
    'Oriental Shorthair',
    'Persa',
    'Pixie-Bob',
    'Ragdoll',
    'Savannah',
    'Scottish Fold',
    'Selkirk Rex',
    'Siamês',
    'Siberiano',
    'Singapura',
    'Sphynx',
    'Tonquinês',
    'Van Turco',
]

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'tutor': forms.Select(attrs={'class': 'form-select'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-select', 'onchange': 'atualizarRacas()'}),
            'raca': forms.Select(attrs={'class': 'form-select'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'microchip': forms.TextInput(attrs={'class': 'form-control'}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['raca'].widget = forms.Select(choices=[('', '--- Selecione uma espécie ---')])
        
        
class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = '__all__'
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'data_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'motivo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Vacinação, Exame de rotina...'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Informações adicionais sobre o animal ou agendamento'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        
class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        exclude = ['paciente']
        widgets = {
            'agendamento': forms.Select(attrs={'class': 'form-select'}),
            'data_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
            'anamnese': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'exame_fisico': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'exames_solicitados': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tratamento': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'retorno_necessario': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'data_retorno': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }