import time

class Order:
    """Representa uma ordem de negociação no sistema."""
    def __init__(self, order_id, tipo, preco, quantidade):
        self.id = order_id          
        self.tipo = tipo            
        self.preco = preco          
        self.quantidade = quantidade 
        self.timestamp = time.time() 

    def __repr__(self):
        return f"Order(ID={self.id}, Tipo={self.tipo}, Preço={self.preco}, Qtd={self.quantidade})"


class Node:
    """Nó base para as estruturas de dados encadeadas."""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None 


class Queue:
    """
    Fila de Entrada (FIFO) para aguardar o processamento pelo motor.
    Deve garantir complexidade O(1) nas operações de extremidade.
    """
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, order):
        """Adiciona uma ordem ao final da fila."""
        new_node = Node(order)
        
        if self.is_empty():
            # Se a fila está vazia, o novo nó é head e tail
            self.head = new_node
            self.tail = new_node
        else:
            # Caso contrário, liga o tail atual ao novo nó e atualiza tail
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        """Remove e retorna a ordem do início da fila."""
        if self.is_empty():
            return None
        
        # Obtém a ordem do head
        order = self.head.data
        
        # Move head para o próximo nó
        self.head = self.head.next
        
        # Se a fila ficou vazia, limpa tail também (evita nós órfãos)
        if self.head is None:
            self.tail = None
        
        return order
        
    def is_empty(self):
        return self.head is None


class DoublyLinkedList:
    """
    Lista Duplamente Encadeada Ordenada para o Livro de Ofertas.
    Inserção ordenada percorrendo os nós terá complexidade O(n).
    """
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_ordered(self, order, is_buy_list):
        """
        Insere de forma ordenada.
        Se is_buy_list == True: ordem decrescente de preço (melhor comprador no início).
        Se is_buy_list == False: ordem crescente de preço (melhor vendedor no início).

        Assume que ordens chegam em ordem cronológica crescente de timestamp.
        Isso garante que, para preços iguais, a ordem mais antiga sempre
        precede a mais nova (comportamento FIFO dentro do mesmo nível de preço).
        """
        novo = Node(order)

        # Caso 1: lista vazia
        if self.head is None:
            self.head = novo
            self.tail = novo
            return

        # Define a comparação de acordo com o tipo de livro.
        
        if is_buy_list:
            melhor = lambda novo_p, atual_p: novo_p > atual_p   # decrescente
        else:
            melhor = lambda novo_p, atual_p: novo_p < atual_p   # crescente

        
        if melhor(order.preco, self.head.data.preco):
            novo.next = self.head
            self.head.prev = novo
            self.head = novo
            return

        atual = self.head

        while atual.next is not None and (
            melhor(atual.next.data.preco, order.preco) or (
                atual.next.data.preco == order.preco and
                atual.next.data.timestamp < order.timestamp)
        ):
            atual = atual.next

        if atual.next is None:
            # Caso 3: chegou ao fim — novo nó é o pior do livro, vira tail
            atual.next = novo
            novo.prev = atual
            self.tail = novo
        else:
            # Caso 4: inserção no meio — religar 4 ponteiros sem criar nós órfãos.
            novo.next = atual.next     
            novo.prev = atual          
            atual.next.prev = novo     
            atual.next = novo           

    def remove(self, order_id):
        """
        Remove um nó de qualquer ponto da lista.
        Retorna o objeto Order removido, ou None se o ID não for encontrado.
        """
        atual = self.head

        while atual is not None:
            if atual.data.id == order_id:

                if atual.prev is None and atual.next is None:
                    # Único nó da lista
                    self.head = None
                    self.tail = None

                elif atual.prev is None:
                    # Nó é o head — promove o seguinte
                    self.head = atual.next
                    self.head.prev = None

                elif atual.next is None:
                    # Nó é o tail — promove o anterior
                    self.tail = atual.prev
                    self.tail.next = None

                else:
                    # Nó do meio — religar predecessor e sucessor diretamente
                    atual.prev.next = atual.next
                    atual.next.prev = atual.prev

                return atual.data   
            atual = atual.next

        return None 
    
    def peek_best_offer(self):
        """Retorna o início da lista (melhor comprador/vendedor) para o motor de match."""
        if self.head:
            return self.head.data
        return None


class Stack:
    """
    Sistema de Undo (Pilha/Stack) para armazenar IDs inseridos com sucesso.
    Deve garantir complexidade O(1) nas operações.
    """
    def __init__(self):
        self.top = None

    def push(self, order_id):
        """Armazena o ID de uma ordem inserida."""
        new_node = Node(order_id)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        """Remove e retorna o último ID inserido para cancelamento."""
        if self.top is None:
            return None
        order_id = self.top.data
        self.top = self.top.next
        return order_id

    def is_empty(self):
        return self.top is None