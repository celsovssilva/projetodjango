from . models import hellen 
from django.shortcuts import redirect, render, get_object_or_404
from .forms import TarefaForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required 



# Create your views here.
@login_required
def home(request):
    search= request.GET.get('search')
    filter= request.GET.get('filter')

    if search:
        tasks= hellen.objects.filter(title__icontains= search, user= request.user)
        
   
   
    else:
        if filter == 'doing':
            task_list = task_list.filter(done='doing')
        elif filter == 'done':
            task_list = task_list.exclude(done='doing')  



        taskList = hellen.objects.all().order_by('-created_at').filter(user= request.user)
        paginator = Paginator(taskList,3)
        page = request.GET.get('page')
        tasks= paginator.get_page(page)
    return render(request, 'hellen/home.html', {'task': tasks, 'search': search, 'filter': filter})

@login_required
def hnp(request,id):
    hn= get_object_or_404(hellen, pk=id)
    return render(request,'hellen/hnp.html', {'hn': hn})
@login_required
def novat(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)

        if form.is_valid():
            tf= form.save(commit=False)
            tf.done = 'doing'
            tf.user= request.user 
            tf.save()
            return redirect('/')

    else:
        form= TarefaForm()
        return render(request, 'hellen/addtarefa.html', {'form': form})
    
@login_required
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
    
@login_required
def deleteTask(request, id):
  task= get_object_or_404(hellen,pk=id)
  task.delete()  
  messages.info(request,"tarefa deletada")

  return redirect('/')

@login_required
def status(request, id):
    task= get_object_or_404(hellen,pk=id)

    if task.done == 'doing':
        task.done = 'done'
        messages.success(request, "tarefa concluida")
    else:
        task.done = 'doing'
        messages.success(request, "tarefa em andamento")
    
    task.save()
    return redirect('/')