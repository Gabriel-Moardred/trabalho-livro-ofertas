from structs import Order, Queue, DoublyLinkedList, Stack

def tentar_match(livro_compras, livro_vendas):
    """
    Motor de cruzamento: verifica as extremidades dos livros e realiza a 
    transação até que os preços não batam ou uma das listas fique vazia.
    """
    while True:
        melhor_compra = livro_compras.peek_best_offer()
        melhor_venda = livro_vendas.peek_best_offer()

        # Verifica se as duas pontas existem e se o preço cruza
        if melhor_compra and melhor_venda and melhor_compra.preco >= melhor_venda.preco:
            # A quantidade negociada é o menor volume entre as duas pontas
            qtd_negociada = min(melhor_compra.quantidade, melhor_venda.quantidade)
            
            print(f"  -> MATCH! Comprador {melhor_compra.id} x Vendedor {melhor_venda.id} | Preço Executado: R$ {melhor_venda.preco:.2f} | Volume: {qtd_negociada}")
            
            # Abate o saldo de ambas as ordens
            melhor_compra.quantidade -= qtd_negociada
            melhor_venda.quantidade -= qtd_negociada

            # Se a ordem de compra zerar, remove do topo do livro
            if melhor_compra.quantidade == 0:
                print(f"     * Ordem de compra {melhor_compra.id} esgotada e removida do livro.")
                livro_compras.remove(melhor_compra.id)
                
            # Se a ordem de venda zerar, remove do topo do livro
            if melhor_venda.quantidade == 0:
                print(f"     * Ordem de venda {melhor_venda.id} esgotada e removida do livro.")
                livro_vendas.remove(melhor_venda.id)
        else:
            # Preços não cruzam mais ou um dos lados do livro acabou
            break

def main():
    print("Iniciando Simulador de Livro de Ofertas...\n")

    # 1. Instanciando as estruturas principais
    fila_entrada = Queue()
    livro_compras = DoublyLinkedList()
    livro_vendas = DoublyLinkedList()
    sistema_undo = Stack()

    # 2. Criando algumas ordens de exemplo com um cenário mais completo
    ordem1 = Order(1, 'C', 15.50, 100) # Compra grande
    ordem2 = Order(2, 'V', 15.00, 50)  
    ordem_test_low = Order(7,'C',12.00, 200)
    ordem_test_low2 = Order(7,'V',15.00, 200)# Venda menor (vai abater parte da ordem 1)
    ordem3 = Order(3, 'C', 14.80, 200) # Compra fora de preço (não vai dar match)
    ordem4 = Order(4, 'V', 15.30, 80)  # Venda que vai abater o resto da ordem 1

    # 3. As ordens entram na Fila FIFO
    print("Enfileirando ordens...")
    fila_entrada.enqueue(ordem1)
    fila_entrada.enqueue(ordem2)
    fila_entrada.enqueue(ordem_test_low)
    fila_entrada.enqueue(ordem3)
    fila_entrada.enqueue(ordem4)
    fila_entrada.enqueue(ordem_test_low2)


    # 4. Processamento contínuo: A cada ordem que entra no livro, tenta buscar um match
    print("\n=== INICIANDO MOTOR DE PROCESSAMENTO ===")
    while not fila_entrada.is_empty():
        ordem_atual = fila_entrada.dequeue()
        print(f"\n[+] Entrando no sistema: {ordem_atual}")
        
        # Inserção segura
        if ordem_atual.tipo == 'C':
            livro_compras.insert_ordered(ordem_atual, is_buy_list=True)
        else:
            livro_vendas.insert_ordered(ordem_atual, is_buy_list=False)
            
        # Registra sucesso na Pilha de Undo
        sistema_undo.push(ordem_atual.id)
        
        # O motor de match precisa rodar IMEDIATAMENTE após cada inserção
        tentar_match(livro_compras, livro_vendas)

    # 5. Demonstração do Sistema de Undo (Cancelamento)
    print("\n=== DEMONSTRAÇÃO DE UNDO (CANCELAMENTO) ===")
    ordem_erro = Order(99, 'C', 10.00, 500) # Ordem isolada, não vai dar match imediato
    
    print(f"Inserindo ordem por engano: {ordem_erro}")
    fila_entrada.enqueue(ordem_erro)
    
    ordem_atual = fila_entrada.dequeue()
    livro_compras.insert_ordered(ordem_atual, is_buy_list=True)
    sistema_undo.push(ordem_atual.id)
    print("Ordem inserida com sucesso no livro de compras.")
    
    print("\n...Solicitação de cancelamento recebida!")
    id_para_cancelar = sistema_undo.pop()
    print(f"Desempilhando ID salvo: {id_para_cancelar}")
    
    # Tenta remover do livro de compras, se não encontrar, tenta no de vendas
    removido = livro_compras.remove(id_para_cancelar)
    if not removido:
         removido = livro_vendas.remove(id_para_cancelar)
         
    if removido:
        print(f"[Sucesso] A ordem {removido.id} foi encontrada e desfeita (removida do livro) em O(n).")
    else:
        print("Falha ao desfazer: ID não encontrado.")

if __name__ == "__main__":
    main()