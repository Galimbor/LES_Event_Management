from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
# Create your views here.


def registar(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        nome = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        user = User.objects.create_user(nome, email, password)
        user.save()
        return redirect('Evento:eventos')

    context = {
        'form': form
    }
    return render(request, 'Login/registar.html', context)