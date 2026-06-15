from structs import Order, Queue, DoublyLinkedList, Stack

def main():
    print("Iniciando Simulador de Livro de Ofertas...\n")

    # 1. Instanciando as estruturas principais
    fila_entrada = Queue()
    livro_compras = DoublyLinkedList()
    livro_vendas = DoublyLinkedList()
    sistema_undo = Stack()

    # 2. Criando algumas ordens de exemplo
    ordem1 = Order(1, 'C', 15.50, 100)
    ordem2 = Order(2, 'V', 15.00, 50)
    ordem3 = Order(3, 'C', 14.80, 200)

    # 3. As ordens entram na Fila FIFO
    print("Enfileirando ordens...")
    fila_entrada.enqueue(ordem1)
    fila_entrada.enqueue(ordem2)
    fila_entrada.enqueue(ordem3)

    # 4. Motor de Processamento (Simulação)
    print("\nProcessando fila de entrada...")
    while not fila_entrada.is_empty():
        # Retira da fila para processar
        ordem_atual = fila_entrada.dequeue()
        
        # Simulação de inserção segura para testar a estrutura
        try:
            if ordem_atual.tipo == 'C':
                livro_compras.insert_ordered(ordem_atual, is_buy_list=True)
            else:
                livro_vendas.insert_ordered(ordem_atual, is_buy_list=False)
            
            # Registra sucesso no Undo
            sistema_undo.push(ordem_atual.id)
            print(f"Ordem {ordem_atual.id} processada com sucesso.")
            
        except Exception as e:
            print(f"Ainda é necessário implementar a inserção! (Erro: {e})")
            break # Interrompe a simulação até que as funções sejam construídas

    # 5. Tentativa de Match de Ordens
    print("\nVerificando Match de Ordens...")
    melhor_compra = livro_compras.peek_best_offer()
    melhor_venda = livro_vendas.peek_best_offer()

    if melhor_compra and melhor_venda:
        # Verifica se preço de compra atende ao preço de venda
        if melhor_compra.preco >= melhor_venda.preco:
            print(f"MATCH ENCONTRADO! Comprador {melhor_compra.id} e Vendedor {melhor_venda.id}")
             #TODO # O grupo implementará a transação e atualização dos nós aqui
        else:
            print("Sem match no momento. Os preços não cruzaram.")

if __name__ == "__main__":
    main()