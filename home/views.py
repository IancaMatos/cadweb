from django.shortcuts import render, redirect
from django.contrib import messages  # <--- Importação necessária do slide
from .models import *
from .forms import *
from django.http import JsonResponse
from django.apps import apps


# ************************************Categoria******************************************* 
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
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            # Mensagem de sucesso adicionada
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('cliente')
    else:
        form = ClienteForm()
    
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
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            # Mensagem de sucesso adicionada
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('cliente')
    else:
        form = ClienteForm(instance=cliente)
        
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
    contexto = {
        'lista': Produto.objects.all().order_by('-id'),
    }
    return render(request, 'produto/lista.html', contexto)

def form_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('produto')
    else:
        form = ProdutoForm()
    return render(request, 'produto/formulario.html', {'form': form})

def editar_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('produto')

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('produto')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produto/formulario.html', {'form': form})

def remover_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
        produto.delete()
        messages.success(request, 'Registro excluído com sucesso')
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
    return redirect('produto')

def detalhes_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
        return render(request, 'produto/detalhes.html', {'produto': produto})
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('produto')
    
    
# ************************************Estoque*******************************************  
def ajustar_estoque(request, id):
    produto = produto = Produto.objects.get(pk=id)
    estoque = produto.estoque # pega o objeto estoque relacionado ao produto
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            estoque = form.save()
            lista = []
            lista.append(estoque.produto) 
            return render(request, 'produto/lista.html', {'lista': lista})
    else:
         form = EstoqueForm(instance=estoque)
    return render(request, 'produto/ajustar_estoque.html', {'form': form,})





# ************************************Testes*******************************************  
def teste1(request):
     return render(request,'testes/teste1.html')


def teste2(request):
     return render(request,'testes/teste2.html')


def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '') # pega o termo digitado
    try:
        # Divida o app e o modelo
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)
    
    # Verifica se o modelo possui os campos 'nome' e 'id'
    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)


# ************************************Pedido******************************************* 
def pedido(request):
    lista = Pedido.objects.all().order_by('-id')  # Obtém todos os registros
    return render(request, 'pedido/lista.html', {'lista': lista})


# ************************************NOVO Pedido******************************************* 
def novo_pedido(request,id):
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            # Caso o registro não seja encontrado, exibe a mensagem de erro
            messages.error(request, 'Registro não encontrado')
            return redirect('cliente')  # Redireciona para a listagem
        # cria um novo pedido com o cliente selecionado
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)# cria um formulario com o novo pedido
        return render(request, 'pedido/formulario.html',{'form': form,})
    else: # se for metodo post, salva o pedido.
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            return redirect('pedido')
        
# ************************************Detalhe Pedido******************************************* 
def detalhes_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')  # Redireciona para a listagem    
    
    if request.method == 'GET':
        itemPedido = ItemPedido(pedido=pedido)
        form = ItemPedidoForm(instance=itemPedido)
    else:
        form = ItemPedidoForm(request.POST)
        # aguardando implementação POST, salvar item
    
    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/detalhes.html',contexto )























 




















