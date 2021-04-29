from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User as Usuario, Admin, ProponenteExterno, ProponenteInterno, Servicostecnicos, Gcp


# Create your views here.


def registar(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        primeiro_nome = request.POST.get('primeiro-nome')
        ultimo_nome = request.POST.get('ultimo-nome')
        morada = request.POST.get('morada')
        nif = request.POST.get('contribuinte')
        data = request.POST.get('data')
        tipo = request.POST.get('usuario')

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        gcpID = None
        internoID = None
        serviosID = None
        adminID = None
        externoID = None

        if tipo == 'gcp':
            gcpID = Gcp()
            gcpID.save()
        elif tipo == 'interno':
            internoID = ProponenteInterno()
            internoID.save()
        elif tipo == 'externo':
            externoID = ProponenteExterno()
            externoID.save()
        elif tipo == 'servicos':
            serviosID = Servicostecnicos()
            serviosID.save()

        usuario = Usuario(first_name=primeiro_nome, last_name=ultimo_nome, morada=morada, contribuinte=nif,
                          datanascimento=data, adminid=adminID, gcpid=gcpID, proponente_internoid=internoID,
                          proponente_externoid=externoID, servicostecnicosid=serviosID, username=username,
                          password=password, email=email)
        usuario.save()

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('Utilizadores:login')

    context = {
        'form': form
    }
    return render(request, 'Login/registar.html', context)


def login(request):
    if request.method == 'POST':
        user = request.POST['username']
        passw = request.POST['password']
        user = authenticate(request, username=user, password=passw)
        if user is not None:
            auth_login(request, user)
            return redirect('Evento:eventos')
        else:
            context = {
                'message': 'Wrong Credentials!'
            }
            return render(request, 'Login/login.html', context)
    return render(request, 'Login/login.html')


def logout_view(request):
    auth_logout(request)
    url = reverse("Evento:eventos")
    return redirect(url, args=(), kwargs={})
