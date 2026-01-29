from django.shortcuts import render, redirect
from django.contrib import messages  # <--- Importação necessária do slide
from .models import *
from .forms import *
from django.http import JsonResponse
from django.apps import apps
from django.contrib.auth.decorators import login_required


# ************************************Categoria******************************************* 

@login_required
def index(request):
    return render(request, 'index.html')
@login_required
def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html', contexto)

@login_required
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

@login_required
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

@login_required
def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        categoria.delete()
        messages.success(request, 'Exclusão realizada com Sucesso')
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        
    return redirect('categoria')

@login_required
def detalhes_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('categoria')

    return render(request, 'categoria/detalhes.html', {'categoria': categoria})


# ************************************Cliente******************************************* 

@login_required
def cliente(request):
    contexto = {
        'lista': Cliente.objects.all().order_by('-id'),
    }
    return render(request, 'cliente/lista.html', contexto)

@login_required
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

@login_required
def detalhes_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('cliente')

    return render(request, 'cliente/detalhes.html', {'cliente': cliente})

@login_required
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

@login_required
def remover_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
        cliente.delete()
        messages.success(request, 'Exclusão realizada com Sucesso')
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        
    return redirect('cliente')

# ************************************Produto******************************************* 

@login_required
def produto(request):
    contexto = {
        'lista': Produto.objects.all().order_by('-id'),
    }
    return render(request, 'produto/lista.html', contexto)

@login_required
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

@login_required
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

@login_required
def remover_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
        produto.delete()
        messages.success(request, 'Registro excluído com sucesso')
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
    return redirect('produto')

@login_required
def detalhes_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
        return render(request, 'produto/detalhes.html', {'produto': produto})
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('produto')
    
    
# ************************************Estoque*******************************************  

@login_required
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

@login_required
def teste1(request):
     return render(request,'testes/teste1.html')

@login_required
def teste2(request):
     return render(request,'testes/teste2.html')

@login_required
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

@login_required
def pedido(request):
    lista = Pedido.objects.all().order_by('-id')  # Obtém todos os registros
    return render(request, 'pedido/lista.html', {'lista': lista})


# ************************************NOVO Pedido******************************************* 

@login_required
def novo_pedido(request, id):
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            messages.error(request, 'Registro não encontrado')
            return redirect('cliente')
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)
        return render(request, 'pedido/formulario.html', {'form': form})
    else:
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            # --- ALTERAÇÃO AQUI (Slide Extras) ---
            # Ao invés de voltar para a lista ('pedido'), vai para os detalhes adicionar itens
            return redirect('detalhes_pedido', id=pedido.id)
        
# ************************************Detalhe Pedido******************************************* 

@login_required
def detalhes_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')

    if request.method == 'GET':
        itemPedido = ItemPedido(pedido=pedido)
        form = ItemPedidoForm(instance=itemPedido)
    else:
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False) # [cite: 21]
            item_pedido.preco = item_pedido.produto.preco # [cite: 23]
            
            # Tratamento de Estoque [cite: 26]
            estoque_atual = item_pedido.produto.estoque
            
            # Verifica se há estoque suficiente [cite: 27]
            if estoque_atual.qtde < item_pedido.qtde:
                messages.error(request, 'Estoque insuficiente para este produto') # [cite: 28]
            else:
                # Decrementa o estoque [cite: 31]
                estoque_atual.qtde -= item_pedido.qtde
                estoque_atual.save() # Salva a alteração no estoque
                
                item_pedido.save() # Salva o item do pedido [cite: 33]
                messages.success(request, 'Produto adicionado com sucesso') # [cite: 43]
                return redirect('detalhes_pedido', id=id)

    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/detalhes.html', contexto)

@login_required
def editar_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')
    
    pedido = item_pedido.pedido
    quantidade_anterior = item_pedido.qtde # Armazena a quantidade anterior [cite: 55]

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            item_pedido = form.save(commit=False)
            
            # Lógica de atualização de estoque na edição [cite: 61]
            estoque = item_pedido.produto.estoque
            
            # Devolvemos a quantidade anterior ao estoque para recalcular
            estoque.qtde += quantidade_anterior 
            
            # Verificamos se o estoque (agora cheio) suporta a nova quantidade [cite: 57]
            if estoque.qtde < item_pedido.qtde:
                messages.error(request, 'Estoque insuficiente para a nova quantidade') # [cite: 59]
                # Reverte o estoque ao estado original (opcional, mas seguro)
                estoque.qtde -= quantidade_anterior
            else:
                # Consome a nova quantidade
                estoque.qtde -= item_pedido.qtde
                estoque.save()
                item_pedido.save()
                messages.success(request, 'Item atualizado com sucesso')
                return redirect('detalhes_pedido', id=pedido.id) # [cite: 64]
                
    else:
        form = ItemPedidoForm(instance=item_pedido)
    
    contexto = {
        'pedido': pedido,
        'form': form,
        'item_pedido': item_pedido, # para exibir qual item está sendo editado
    }
    return render(request, 'pedido/detalhes.html', contexto)

@login_required
def remover_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
        pedido_id = item_pedido.pedido.id
        estoque = item_pedido.produto.estoque
        
        # Devolve a quantidade ao estoque antes de excluir [cite: 78]
        estoque.qtde += item_pedido.qtde
        estoque.save()
        
        item_pedido.delete()
        messages.success(request, 'Item removido com sucesso')
        
        return redirect('detalhes_pedido', id=pedido_id)
        
    except ItemPedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')