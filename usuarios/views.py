from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from tenants.models import Domain
from django.contrib import messages
from django.urls import reverse

class CustomLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'usuarios/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Pega o schema (empresa) do usuário
            tenant = user.tenant  # ou user.empresa se usar esse nome
            domain = Domain.objects.filter(tenant=tenant).first()
            if domain:
                return redirect(f'http://{domain.domain}:8000{reverse("dashboard")}')
            else:
                messages.error(request, "Domínio da empresa não encontrado.")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
        return render(request, 'usuarios/login.html', {'form': form})