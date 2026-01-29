import locale
from django.db import models
from datetime import datetime
import random
from decimal import Decimal # <--- IMPORTAÇÃO NECESSÁRIA

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()

    def __str__(self):
        return self.nome
    
# ************************************Cliente*******************************************
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, verbose_name="C.P.F")
    datanasc = models.DateField(verbose_name="Data de Nascimento")

    def __str__(self):
        return self.nome
    
    @property
    def datanascimento(self):
        """Retorna a data de nascimento no formato DD/MM/AAAA"""
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return None

# ************************************Produto*******************************************
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    img_base64 = models.TextField(blank=True)

    def __str__(self):
        return self.nome
    
    @property
    def estoque(self):
        # Tenta buscar o estoque, se não existir, cria um novo com qtde 0
        estoque_item, flag_created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        return estoque_item
    

# ************************************Estoque*******************************************
class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()

    def __str__(self):
        return f'{self.produto.nome} - Quantidade: {self.qtde}'
    

# ************************************Pedido*******************************************
class Pedido(models.Model):
    NOVO = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4

    STATUS_CHOICES = [
        (NOVO, 'Novo'),
        (EM_ANDAMENTO, 'Em Andamento'),
        (CONCLUIDO, 'Concluído'),
        (CANCELADO, 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOVO)

    def __str__(self):
            return f"Pedido {self.id} - Cliente: {self.cliente.nome} - Status: {self.get_status_display()}"

    @property
    def data_pedidof(self):
        if self.data_pedido:
            return self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return None

    @property
    def total(self):
        """Calcula o total de todos os itens no pedido"""
        # Se não houver itens, retorna Decimal(0)
        soma = sum(item.total for item in self.itempedido_set.all())
        return soma if soma else Decimal('0.00')

    @property
    def qtdeItens(self):
        """Conta a qtde de itens no pedido"""
        return self.itempedido_set.count()
    
    # --- Propriedades de Pagamento ---

    @property
    def pagamentos(self):
        return Pagamento.objects.filter(pedido=self)    
    
    @property
    def total_pago(self):
        soma = sum(pagamento.valor for pagamento in self.pagamentos.all())
        return soma if soma else Decimal('0.00')
    
    @property
    def debito(self):
        return self.total - self.total_pago

    # --- Cálculos de Impostos (Desafio Nota Fiscal) ---
    # Convertemos os números float para Decimal('string') para evitar erro de tipo
    @property
    def icms(self):
        return self.total * Decimal('0.18') # 18%

    @property
    def ipi(self):
        return self.total * Decimal('0.04') # 4%

    @property
    def pis(self):
        return self.total * Decimal('0.0165') # 1.65%
    
    @property
    def cofins(self):
        return self.total * Decimal('0.076') # 7.6%

    @property
    def total_impostos(self):
        """Soma de todos os impostos calculados"""
        return self.icms + self.ipi + self.pis + self.cofins

    @property
    def total_com_impostos(self):
        """Total dos produtos + impostos"""
        return self.total + self.total_impostos

    @property
    def chave_acesso(self):
        """Gera uma chave de acesso aleatória para a NF"""
        ano = datetime.now().year
        # Gera um número aleatório grande para simular a chave
        random_part = random.randint(100000000000000000000000000000, 999999999999999999999999999999)
        return f"{ano}{self.id:04d}{random_part}"


# ************************************Pagamento*******************************************
class Pagamento(models.Model):
    DINHEIRO = 1
    CARTAO = 2
    PIX = 3
    OUTRA = 4

    FORMA_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CARTAO, 'Cartão'),
        (PIX, 'Pix'),
        (OUTRA, 'Outra'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    data_pgto = models.DateTimeField(auto_now_add=True)
    
    @property
    def data_pgtof(self):
        """Retorna a data no formato DD/MM/AAAA HH:MM"""
        if self.data_pgto:
            return self.data_pgto.strftime('%d/%m/%Y %H:%M')
        return None


# ************************************ItemPedido*******************************************
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produto.nome} (Qtd: {self.qtde}) - Preço Unitário: {self.preco}"    

    @property
    def total(self):
        """Calcula o total do item (qtde * preco)"""
        return self.qtde * self.preco