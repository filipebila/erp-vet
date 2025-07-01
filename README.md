# 🐾 ERP Veterinário - ITM Vet

Sistema de gestão moderno e inteligente para clínicas e hospitais veterinários, com foco em praticidade, eficiência e integração com inteligência artificial.

## 📌 Status Atual do Projeto

✅ Sistema multiempresa funcionando com `django-tenants`  
✅ Autenticação personalizada com redirecionamento para schema  
✅ Landing page pública com login  
✅ Módulos: Tutores, Pacientes, Agendamentos, Consultas  
✅ Upload de fotos e vídeos por consulta  
✅ Transcrição de observações por voz com OpenAI Whisper  
✅ Análise crítica do atendimento via GPT-4  
✅ Visual da análise com accordion e nova view  
✅ Git versionado para uso em múltiplas máquinas

---

## 🚀 Tecnologias Utilizadas

- Python 3.12
- Django 5.2 com `django-tenants`
- PostgreSQL
- Bootstrap 5
- OpenAI API (Whisper + GPT-4)
- HTML, CSS

---

## 🛠️ Instalação (modo desenvolvimento)

### 1. Clonar o projeto

```bash
git clone https://github.com/filipebila/erp-vet.git
cd erp-vet
```

### 2. Criar ambiente virtual

```bash
python -m venv env
source env/bin/activate   # Linux/macOS
env\Scripts\activate      # Windows
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Criar banco PostgreSQL

```sql
CREATE DATABASE itm_vet_db;
CREATE USER admin_itm WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE itm_vet_db TO admin_itm;
```

### 5. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Preencher `OPENAI_API_KEY` no `.env`.

### 6. Executar migrações

```bash
python manage.py migrate_schemas --shared
```

### 7. Criar Tenant

```bash
python manage.py shell
```

```python
from tenants.models import Client, Domain
empresa = Client.objects.create(nome="Empresa Modelo", cnpj="00.000.000/0001-00", pago_ate="2099-12-31", ativo=True, schema_name="empresa_modelo")
Domain.objects.create(domain="empresa-modelo.localhost", tenant=empresa, is_primary=True)
```

```bash
python manage.py migrate_schemas --tenant
python manage.py createsuperuser --schema=empresa_modelo
```

### 8. Rodar servidor

```bash
python manage.py runserver
```

Acesse:

- http://localhost:8000/
- http://empresa-modelo.localhost:8000/

> Adicione no `/etc/hosts` ou `C:\Windows\System32\drivers\etc\hosts`:

```
127.0.0.1   empresa-modelo.localhost
```

---

## 📋 Funcionalidades Atuais

- Gestão de Tutores, Pacientes e Agendamentos
- Atendimento clínico com transcrição de voz
- Upload de imagens e vídeos na consulta
- Análise inteligente por IA (GPT-4)
- Interface responsiva com Bootstrap
- Suporte a múltiplas clínicas (multi-tenant)

---

## 🔮 Futuras Funcionalidades

- Geração de PDF do atendimento
- Relatórios e indicadores visuais
- Integração com WhatsApp
- Painel financeiro e faturamento

---

## 👨‍💻 Contato

Desenvolvido por **Filipe Bila**  
GitHub: [@filipebila](https://github.com/filipebila)  
LinkedIn: [linkedin.com/in/filipebila](https://linkedin.com/in/filipebila)

---

