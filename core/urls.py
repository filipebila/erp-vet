from django.urls import path
from . import views
from .views import AtendimentoConsultaView, AgendamentosDoDiaView, iniciar_consulta, landing_view, dashboard_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('', landing_view, name='landing'),
    
    path('dashboard/', dashboard_view, name='dashboard'),
    
    path('login/', auth_views.LoginView.as_view(template_name='core/landing.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('tutores/', views.TutorListView.as_view(), name='tutores-list'),
    path('tutores/novo/', views.TutorCreateView.as_view(), name='tutor-create'),
    path('tutores/<int:pk>/', views.TutorDetailView.as_view(), name='tutor-detail'),
    path('tutores/<int:pk>/editar/', views.TutorUpdateView.as_view(), name='tutor-update'),
    path('tutores/<int:pk>/excluir/', views.TutorDeleteView.as_view(), name='tutor-delete'),
    
    path('pacientes/', views.PacienteListView.as_view(), name='pacientes-list'),
    path('pacientes/novo/', views.PacienteCreateView.as_view(), name='paciente-create'),
    path('pacientes/<int:pk>/', views.PacienteDetailView.as_view(), name='paciente-detail'),
    path('pacientes/<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='paciente-update'),
    path('pacientes/<int:pk>/excluir/', views.PacienteDeleteView.as_view(), name='paciente-delete'),
    
    path('agendamentos/', views.AgendamentoListView.as_view(), name='agendamentos-list'),
    path('agendamentos/novo/', views.AgendamentoCreateView.as_view(), name='agendamentos-create'),
    path('agendamentos/<int:pk>/', views.AgendamentoDetailView.as_view(), name='agendamentos-detail'),
    path('agendamentos/<int:pk>/editar/', views.AgendamentoUpdateView.as_view(), name='agendamentos-update'),
    path('agendamentos/<int:pk>/excluir/', views.AgendamentoDeleteView.as_view(), name='agendamentos-delete'),
    
    path('consultas/', views.ConsultaListView.as_view(), name='consultas-list'),
    path('consultas/novo/', views.ConsultaCreateView.as_view(), name='consultas-create'),
    path('consultas/<int:pk>/', views.ConsultaDetailView.as_view(), name='consultas-detail'),
    #path('consultas/<int:pk>/editar/', views.ConsultaUpdateView.as_view(), name='consultas-update'),
    path('consultas/<int:pk>/excluir/', views.ConsultaDeleteView.as_view(), name='consultas-delete'),
    path('consultas/hoje/', AgendamentosDoDiaView.as_view(), name='agendamentos-hoje'),
    path('consultas/iniciar/<int:agendamento_id>/', iniciar_consulta, name='iniciar-consulta'),
    
    path('consultas/<int:pk>/atendimento/', AtendimentoConsultaView.as_view(), name='consulta-atendimento'),

]