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
        Se is_buy_list == True: ordem decrescente de preço.
        Se is_buy_list == False: ordem crescente de preço.
        """
        pass # TODO: Implementar religamento de ponteiros sem deixar nós órfãos

    def remove(self, order_id):
        """Remove um nó de qualquer ponto da lista."""
        pass # TODO: Implementar lógica do grupo
        
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
        pass # TODO: Implementar lógica do grupo

    def pop(self):
        """Remove e retorna o último ID inserido para cancelamento."""
        pass # TODO: Implementar lógica do grupo