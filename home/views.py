from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # <--- Importação necessária do slide
from .models import *
from .forms import *

def index(request):
    return render(request, 'index.html')

def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html', contexto)

def form_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            # Mensagem de sucesso adicionada
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('categoria')
    else:
        form = CategoriaForm()
    
    contexto = {
        'form': form,
    }
    return render(request, 'categoria/formulario.html', contexto)

def editar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('categoria')

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            # Mensagem de sucesso adicionada
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('categoria')
    else:
        form = CategoriaForm(instance=categoria)
        
    return render(request, 'categoria/formulario.html', {'form': form})

def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        categoria.delete()
        messages.success(request, 'Exclusão realizada com Sucesso')
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        
    return redirect('categoria')


def detalhes_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('categoria')

    return render(request, 'categoria/detalhes.html', {'categoria': categoria})


# ************************************Cliente******************************************* 

def cliente(request):
    contexto = {
        'lista': Cliente.objects.all().order_by('-id'),
    }
    return render(request, 'cliente/lista.html', contexto)

def form_cliente(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            # Mensagem de sucesso adicionada
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('cliente')
    else:
        form = ProdutoForm()
    
    contexto = {
        'form': form,
    }
    return render(request, 'cliente/formulario.html', contexto)

def detalhes_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('cliente')

    return render(request, 'cliente/detalhes.html', {'cliente': cliente})

def editar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('cliente')

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            # Mensagem de sucesso adicionada
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('cliente')
    else:
        form = ProdutoForm(instance=cliente)
        
    return render(request, 'cliente/formulario.html', {'form': form})

def remover_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
        cliente.delete()
        messages.success(request, 'Exclusão realizada com Sucesso')
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        
    return redirect('cliente')

# ************************************Produto******************************************* 
def produto(request):
    """Lista todos os produtos"""
    contexto = {
        'lista': Produto.objects.all().order_by('-id'),
    }
    return render(request, 'produto/lista.html', contexto)

def form_produto(request):
    """Cria um novo produto"""
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('produto')
        else:
            messages.error(request, 'Erro ao validar o formulário. Verifique os dados.')
    else:
        form = ProdutoForm()
    
    return render(request, 'produto/formulario.html', {'form': form})

def editar_produto(request, id):
    """Edita um produto existente"""
    produto_instancia = get_object_or_404(Produto, pk=id)
    
    if request.method == 'POST':
        # Importante: passar a instância para o formulário salvar no registro correto
        form = ProdutoForm(request.POST, instance=produto_instancia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('produto')
    else:
        # Carrega o formulário preenchido com os dados do produto
        form = ProdutoForm(instance=produto_instancia)
        
    return render(request, 'produto/formulario.html', {'form': form})

def detalhes_produto(request, id):
    """Exibe os detalhes de um único produto"""
    produto_detalhe = get_object_or_404(Produto, pk=id)
    return render(request, 'produto/detalhes.html', {'produto': produto_detalhe})

def remover_produto(request, id):
    """Remove um produto"""
    produto_instancia = get_object_or_404(Produto, pk=id)
    
    if request.method == 'POST' or request.method == 'GET':
        produto_instancia.delete()
        messages.success(request, 'Produto removido com sucesso!')
        
    return redirect('produto')