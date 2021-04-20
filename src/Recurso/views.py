from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import Recurso
from .forms import RecursoForm


# Create your views here.

# def home(request):
#     return render(request, 'inicio.html')


#
# def create_recurso(request):
#     return render(request, 'Recurso/new_recurso.html')
#
#
# class RecursoList(ListView):
#     model = Recurso
#     paginate_by = 10
#
#
# class RecursoCreate(CreateView):
#     model = Recurso
#     fields = ['id']
#     template_name = 'Recurso/create_recurso.html'
#     success_url = reverse_lazy('recurso-list')
#
#
# class RecursoDelete(DeleteView):
#     model = Recurso
#     success_url = reverse_lazy('recurso-list')
#
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)


def home_view(request):
    return render(request, 'inicio.html')


def recursos(request):
    return render(request, 'Recurso/recurso_list.html')


def create_recurso(request):
    form = RecursoForm(request.POST or None)
    print(request.POST)
    print(form)
    if form.is_valid():

        # Evento data
        nome = request.POST.get("nome")
        recurso = Recurso(nome=nome, fonte="Interna")
        recurso.save()
        return redirect('Recurso:recurso_success')
    else:
        print("not valid!")

    context = {
        'form': form
    }
    return render(request, 'Recurso/create_recurso.html', context)


def recurso_success(request):
    return render(request, 'Recurso/create_recurso_success.html')
