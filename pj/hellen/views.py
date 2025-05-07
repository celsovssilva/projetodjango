from . models import hellen 
from django.shortcuts import redirect, render, get_object_or_404
from .forms import TarefaForm
from django.contrib import messages
from django.core.paginator import Paginator



# Create your views here.

def home(request):
    search= request.GET.get('search')

    if search:
        tasks= hellen.objects.filter(title__icontains= search)

   
    else:




        taskList = hellen.objects.all().order_by('-created_at')
        paginator = Paginator(taskList,3)
        page = request.GET.get('page')
        tasks= paginator.get_page(page)
    return render(request, 'hellen/home.html', {'task': tasks})


def hnp(request,id):
    hn= get_object_or_404(hellen, pk=id)
    return render(request,'hellen/hnp.html', {'hn': hn})

def novat(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)

        if form.is_valid():
            tf= form.save(commit=False)
            tf.done = 'doing'
            tf.save()
            return redirect('/')

    else:
        form= TarefaForm()
        return render(request, 'hellen/addtarefa.html', {'form': form})
    

def editTask(request, id ):
    task= get_object_or_404(hellen,pk=id)
    form = TarefaForm(instance=task)

    if request.method=='POST':

        form= TarefaForm(request.POST, instance=task)

        if form.is_valid():
             task.save()
             return redirect('/')
        else:
            return render(request, 'hellen/editi.html', {'form': form, ' task': task})
    else:
        return render(request, 'hellen/editi.html', {'form': form, ' task': task})
    

def deleteTask(request, id):
  task= get_object_or_404(hellen,pk=id)
  task.delete()  
  messages.info(request,"tarefa deletada")

  return redirect('/')
