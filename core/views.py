#core/views.py
import os
import traceback
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy, reverse
from .models import Paciente, Tutor, Agendamento, Consulta, ArquivoConsulta
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import TutorForm, PacienteForm, AgendamentoForm, RACAS_CACHORRO, RACAS_GATO, ConsultaForm # criaremos esse a seguir
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.timezone import localtime
from django.contrib.auth.forms import AuthenticationForm
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv



class TutorListView(ListView):
    model = Tutor
    template_name = 'core/tutores_list.html'
    context_object_name = 'tutores'

class TutorCreateView(CreateView):
    model = Tutor
    form_class = TutorForm
    template_name = 'core/tutor_form.html'
    success_url = reverse_lazy('tutores-list')
    
class TutorDetailView(DetailView):
    model = Tutor
    template_name = 'core/tutor_detail.html'
    context_object_name = 'tutor'

class TutorUpdateView(UpdateView):
    model = Tutor
    form_class = TutorForm
    template_name = 'core/tutor_form.html'
    success_url = reverse_lazy('tutores-list')

class TutorDeleteView(DeleteView):
    model = Tutor
    template_name = 'core/tutor_confirm_delete.html'
    success_url = reverse_lazy('tutores-list')

class PacienteListView(ListView):
    model = Paciente
    template_name = 'core/pacientes_list.html'
    context_object_name = 'pacientes'

class PacienteCreateView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'core/paciente_form.html'
    success_url = reverse_lazy('pacientes-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RACAS_CACHORRO'] = RACAS_CACHORRO
        context['RACAS_GATO'] = RACAS_GATO
        return context
    
class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'core/paciente_detail.html'
    context_object_name = 'paciente'

class PacienteUpdateView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'core/paciente_form.html'
    success_url = reverse_lazy('pacientes-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RACAS_CACHORRO'] = RACAS_CACHORRO
        context['RACAS_GATO'] = RACAS_GATO
        return context

class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'core/paciente_confirm_delete.html'
    success_url = reverse_lazy('pacientes-list')
    
class AgendamentoListView(ListView):
    model = Agendamento
    template_name = 'core/agendamentos_list.html'
    context_object_name = 'agendamentos'

class AgendamentoCreateView(CreateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'core/agendamento_form.html'
    success_url = reverse_lazy('agendamentos-list')

class AgendamentoDetailView(DetailView):
    model = Agendamento
    template_name = 'core/agendamento_detail.html'
    context_object_name = 'agendamento'

class AgendamentoUpdateView(UpdateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'core/agendamento_form.html'
    success_url = reverse_lazy('agendamentos-list')

class AgendamentoDeleteView(DeleteView):
    model = Agendamento
    template_name = 'core/agendamento_confirm_delete.html'
    success_url = reverse_lazy('agendamentos-list')
    
class ConsultaListView(ListView):
    model = Consulta
    template_name = 'core/consultas_list.html'
    context_object_name = 'consultas'

class ConsultaCreateView(CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'core/consulta_form.html'
    success_url = reverse_lazy('consultas-list')

    def form_valid(self, form):
        agendamento = form.cleaned_data['agendamento']
        form.instance.paciente = agendamento.paciente  # Preenche o paciente automaticamente

        response = super().form_valid(form)
        
        agendamento.status = 'Confirmado'
        agendamento.save()

        # Se for necessário retorno, cria novo agendamento
        if form.cleaned_data.get('retorno_necessario'):
            Agendamento.objects.create(
                paciente=agendamento.paciente,
                data_hora=form.cleaned_data.get('data_retorno'),
                motivo='Retorno da consulta',
                status='Pendente' if not form.cleaned_data.get('data_retorno') else 'Confirmado'
            )

        return response


class ConsultaDetailView(DetailView):
    model = Consulta
    template_name = 'core/consulta_detail.html'
    context_object_name = 'consulta'

'''class ConsultaUpdateView(UpdateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'core/consulta_form.html'
    success_url = reverse_lazy('consultas-list')'''

class ConsultaDeleteView(DeleteView):
    model = Consulta
    template_name = 'core/consulta_confirm_delete.html'
    success_url = reverse_lazy('consultas-list')
    
class AtendimentoConsultaView(View):
    template_name = 'core/consulta_atendimento.html'

    def get(self, request, pk):
        consulta = get_object_or_404(Consulta, pk=pk)
        historico = Consulta.objects.filter(paciente=consulta.paciente).exclude(pk=pk)
        return render(request, self.template_name, {
            'consulta': consulta,
            'historico': historico
        })

    def post(self, request, pk):
        consulta = get_object_or_404(Consulta, pk=pk)

        # Atualiza os campos do formulário
        consulta.motivo = request.POST.get("motivo")
        consulta.anamnese = request.POST.get("anamnese")
        consulta.exame_fisico = request.POST.get("exame_fisico")
        consulta.diagnostico = request.POST.get("diagnostico")
        consulta.exames_solicitados = request.POST.get("exames_solicitados")
        consulta.tratamento = request.POST.get("tratamento")
        consulta.observacoes = request.POST.get("observacoes")
        consulta.retorno_necessario = bool(request.POST.get("retorno_necessario"))
        consulta.data_retorno = request.POST.get("data_retorno") or None
        consulta.data_hora = timezone.now()
        consulta.save()

        # Atualiza status do agendamento
        if consulta.agendamento and consulta.agendamento.status != 'Confirmado':
            consulta.agendamento.status = 'Confirmado'
            consulta.agendamento.save()

        # Cria agendamento de retorno, se necessário
        if consulta.retorno_necessario and consulta.data_retorno:
            try:
                data_retorno_formatada = timezone.datetime.fromisoformat(consulta.data_retorno)
            except Exception:
                data_retorno_formatada = None

            if data_retorno_formatada and not Agendamento.objects.filter(
                paciente=consulta.paciente, data_hora=consulta.data_retorno
            ).exists():
                Agendamento.objects.create(
                    paciente=consulta.paciente,
                    data_hora=consulta.data_retorno,
                    motivo='Retorno da consulta',
                    status='Pendente'
                )

        # Upload de múltiplos arquivos, se houver
        for arquivo in request.FILES.getlist("arquivos"):
            tipo = "foto" if arquivo.content_type.startswith("image") else "video"
            tamanho_mb = round(arquivo.size / (1024 * 1024), 2)

            if tipo == "foto" and tamanho_mb > 5:
                messages.warning(request, f"Imagem '{arquivo.name}' maior que 5MB não foi salva.")
                continue

            if tipo == "video" and tamanho_mb > 20:
                messages.warning(request, f"Vídeo '{arquivo.name}' maior que 20MB não foi salvo.")
                continue

            ArquivoConsulta.objects.create(
                consulta=consulta,
                arquivo=arquivo,
                tipo=tipo
            )

        messages.success(request, "Consulta atualizada com sucesso!")
        return redirect("consultas-detail", pk=consulta.pk)
    
class AgendamentosDoDiaView(ListView):
    model = Agendamento
    template_name = 'core/agendamentos_dia.html'
    context_object_name = 'agendamentos_dia'

    def get(self, request, *args, **kwargs):
        print("🔍 Host recebido:", request.get_host())  # Aqui veremos o domínio exato
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        agora = localtime()
        inicio_dia = agora.replace(hour=0, minute=0, second=0, microsecond=0)
        fim_dia = agora.replace(hour=23, minute=59, second=59, microsecond=999999)

        return Agendamento.objects.filter(
            data_hora__range=(inicio_dia, fim_dia)
        ).order_by('data_hora')

def iniciar_consulta(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, pk=agendamento_id)

    # Verifica se já existe consulta vinculada
    if hasattr(agendamento, 'consulta'):
        return HttpResponseRedirect(reverse('consulta-atendimento', args=[agendamento.consulta.pk]))

    # Cria nova consulta vinculada ao agendamento
    consulta = Consulta.objects.create(
        paciente=agendamento.paciente,
        agendamento=agendamento,
        data_hora=agendamento.data_hora,
        motivo=agendamento.motivo
    )

    return HttpResponseRedirect(reverse('consulta-atendimento', args=[consulta.pk]))


def landing_view(request):
    form = AuthenticationForm()
    return render(request, 'core/landing.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


load_dotenv()  # Garante que .env seja lido, útil em dev
@csrf_exempt
#@login_required
def gerar_analise_ia(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    consulta.status_analise_ia = "em_analise"
    consulta.save()

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Base do prompt textual
        prompt_texto = f"""
Você é um veterinário consultor. Avalie o atendimento abaixo e forneça uma análise crítica profissional.

📄 Dados do paciente:
- Nome: {consulta.paciente.nome}
- Espécie: {consulta.paciente.especie}
- Raça: {consulta.paciente.raca}
- Data de nascimento: {consulta.paciente.data_nascimento}

📋 Consulta:
- Motivo: {consulta.motivo}
- Anamnese: {consulta.anamnese}
- Exame físico: {consulta.exame_fisico}
- Diagnóstico: {consulta.diagnostico}
- Exames solicitados: {consulta.exames_solicitados}
- Tratamento: {consulta.tratamento}
- Observações: {consulta.observacoes}

🔎 Sua análise deve incluir:
1. Avaliação do diagnóstico.
2. Possíveis diagnósticos diferenciais.
3. Sugestões de exames adicionais (se necessário).
4. Avaliação da conduta terapêutica.
5. Riscos ou cuidados não abordados.
"""

        # Lista de conteúdos para o modelo (texto + imagens, se houver)
        conteudo_usuario = [{"type": "text", "text": prompt_texto}]

        imagens = consulta.arquivos.filter(tipo='foto')
        if imagens.exists():
            for img in imagens:
                imagem_url = f"{request.scheme}://{request.get_host()}{img.arquivo.url}"
                conteudo_usuario.append({
                    "type": "image_url",
                    "image_url": {"url": imagem_url}
                })

        # Envia para OpenAI com modelo vision
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um especialista em medicina veterinária."},
                {"role": "user", "content": conteudo_usuario}
            ],
            temperature=0.7,
            max_tokens=800
        )

        resultado = response.choices[0].message.content
        consulta.analise_ia = resultado
        consulta.status_analise_ia = "concluida"
        consulta.save()
        messages.success(request, "Análise gerada com sucesso!")

    except Exception as e:
        consulta.status_analise_ia = "erro"
        consulta.save()
        print("❌ ERRO NA ANÁLISE IA:", e)
        traceback.print_exc()
        messages.error(request, f"Ocorreu um erro ao gerar a análise: {str(e)}")

    return redirect('consultas-detail', consulta_id)

@login_required
def analise_ia(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    return render(request, 'core/analise_ia.html', {'consulta': consulta})