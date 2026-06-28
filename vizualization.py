import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QTextEdit, QGroupBox, QLabel)
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtCore import Qt, pyqtSignal, QObject

# Importando as estruturas e main
from structs import Order, Queue, DoublyLinkedList, Stack 
from main import tentar_match 

class EmissorLog(QObject):
    texto_escrito = pyqtSignal(str) 
    def write(self, text):
        self.texto_escrito.emit(str(text)) 
    def flush(self):
        pass 

class LivroOfertasPyQt(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("Simulador - Motor Gráfico PyQt6") 
        self.resize(1100, 750) 
        self.clear = True
        
        self.setStyleSheet("""
            QWidget {
                background-color: #2e3440;a
                color: #d8dee9;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QGroupBox {
                border: 2px solid #4c566a;
                border-radius: 8px;
                margin-top: 1.5ex;
                font-weight: bold;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                color: #88c0d0;
            }
            QLineEdit {
                background-color: #3b4252;
                border: 1px solid #4c566a;
                border-radius: 4px;
                padding: 8px;
                color: #eceff4;
            }
            QLineEdit:focus {
                border: 1px solid #88c0d0;
            }
            QPushButton {
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #5e81ac; 
                opacity: 0.8;
            }
            QTableWidget {
                background-color: #2e3440;
                alternate-background-color: #3b4252;
                gridline-color: #4c566a;
                border: 1px solid #4c566a;
                border-radius: 6px;
            }
            QScrollBar:vertical {
                border: none;
                background: #2e3440;
                width: 12px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #4c566a;
                min-height: 20px;
                border-radius: 6px;
            }
        """)

        self.fila_entrada = Queue() 
        self.livro_compras = DoublyLinkedList() 
        self.livro_vendas = DoublyLinkedList() 
        self.sistema_undo = Stack() 

        self.emissor_log = EmissorLog() 
        self.emissor_log.texto_escrito.connect(self.atualizar_log) 
        sys.stdout = self.emissor_log 

        self.init_ui() 

        # Atalho de teclado para Desfazer (Ctrl+Z)
        self.shortcut_undo = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut_undo.activated.connect(self.desfazer_ordem)

    def init_ui(self):
        widget_central = QWidget() 
        layout_principal = QVBoxLayout(widget_central) 
        layout_principal.setSpacing(20)
        layout_principal.setContentsMargins(20, 20, 20, 20)

        # === Painel de Entrada ===
        grupo_controle = QGroupBox("Painel de Negociação")
        painel_controle = QHBoxLayout(grupo_controle)
        painel_controle.setSpacing(10)

        self.input_id = QLineEdit(); self.input_id.setPlaceholderText("ID da Ordem")

        # Enter mnada a entrega (colocado em todas as caixas)

        self.input_id.returnPressed.connect(self.adicionar_ordem) 
        
        # Botão de alternância (Toggle) no negocio de compra e venda la
        self.btn_tipo = QPushButton("Compra")
        self.btn_tipo.setStyleSheet("""
            QPushButton { background-color: #a3be8c; color: #2e3440; font-weight: bold;}
            QPushButton:hover { background-color: #8fbcbb; }
        """)
        self.btn_tipo.clicked.connect(self.alternar_tipo)



        self.input_preco = QLineEdit(); self.input_preco.setPlaceholderText("Preço (R$)") 
        self.input_preco.returnPressed.connect(self.adicionar_ordem) 
        
        self.input_qtd = QLineEdit(); self.input_qtd.setPlaceholderText("Quantidade") 
        
 
        self.input_qtd.returnPressed.connect(self.adicionar_ordem)
        
        btn_add = QPushButton("Adicionar Ordem") 
        btn_add.setStyleSheet("""
            QPushButton { background-color: #81a1c1; color: #2e3440; }
            QPushButton:hover { background-color: #88c0d0; }
        """)
        btn_add.clicked.connect(self.adicionar_ordem) 

        btn_undo = QPushButton("Desfazer (Undo)") 
        btn_undo.setStyleSheet("""
            QPushButton { background-color: #bf616a; color: #2e3440; }
            QPushButton:hover { background-color: #d08770; }
        """)
        btn_undo.clicked.connect(self.desfazer_ordem) 

        self.btn_clear = QPushButton("Limpar")
        self.btn_clear.setStyleSheet("""
            QPushButton { background-color: #a3be8c; color: #2e3440; font-weight: bold;}
            QPushButton:hover { background-color: #8fbcbb; }
        """)
        self.btn_clear.clicked.connect(self.alternar_clear)

        for widget in [self.input_id, self.btn_tipo, self.input_preco, self.input_qtd, btn_add, btn_undo, self.btn_clear]: 
            painel_controle.addWidget(widget) 
        
        layout_principal.addWidget(grupo_controle)

        # === Tabelas (Livro de Ofertas) ===
        layout_livros = QHBoxLayout() 
        layout_livros.setSpacing(20)

        self.tabela_compras = self.criar_tabela("Compradores", "#a3be8c") 
        self.tabela_vendas = self.criar_tabela("Vendedores", "#bf616a") 
        
        grupo_compras = QVBoxLayout()
        titulo_compras = QLabel("Livro de Compras (Bids)") # Removido o emote
        titulo_compras.setStyleSheet("font-size: 16px; font-weight: bold; color: #a3be8c;")
        titulo_compras.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grupo_compras.addWidget(titulo_compras)
        grupo_compras.addWidget(self.tabela_compras)

        grupo_vendas = QVBoxLayout()
        titulo_vendas = QLabel("Livro de Vendas (Asks)") # Removido o emote
        titulo_vendas.setStyleSheet("font-size: 16px; font-weight: bold; color: #bf616a;")
        titulo_vendas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grupo_vendas.addWidget(titulo_vendas)
        grupo_vendas.addWidget(self.tabela_vendas)

        layout_livros.addLayout(grupo_compras)
        layout_livros.addLayout(grupo_vendas)
        layout_principal.addLayout(layout_livros)

        # === Log do Sistema ===
        grupo_log = QGroupBox("Console de Eventos (Log)")
        layout_log = QVBoxLayout(grupo_log)
        self.caixa_log = QTextEdit() 
        self.caixa_log.setReadOnly(True) 
        self.caixa_log.setStyleSheet("""
            background-color: #262b35; 
            color: #eceff4; 
            font-family: Consolas, monospace;
            border: none;
        """)
        layout_log.addWidget(self.caixa_log)
        layout_principal.addWidget(grupo_log)
        
        self.setCentralWidget(widget_central) 

    def alternar_tipo(self):
        """Alterna visualmente o botão entre Compra (Verde) e Venda (Vermelho)"""
        if self.btn_tipo.text() == "Compra":
            self.btn_tipo.setText("Venda")
            self.btn_tipo.setStyleSheet("""
                QPushButton { background-color: #bf616a; color: #2e3440; font-weight: bold;}
                QPushButton:hover { background-color: #d08770; }
            """)
        else:
            self.btn_tipo.setText("Compra")
            self.btn_tipo.setStyleSheet("""
                QPushButton { background-color: #a3be8c; color: #2e3440; font-weight: bold;}
                QPushButton:hover { background-color: #8fbcbb; }
            """)
    def alternar_clear(self):
        """Alterna visualmente o botão entre Compra (Verde) e Venda (Vermelho)"""
        if self.btn_clear.text() == "Limpar":
            self.btn_clear.setText("N Limpar")
            self.clear = False
            self.btn_clear.setStyleSheet("""
                QPushButton { background-color: #bf616a; color: #2e3440; font-weight: bold;}
                QPushButton:hover { background-color: #d08770; }
            """)
        else:
            self.btn_clear.setText("Limpar")
            self.clear = True
            self.btn_clear.setStyleSheet("""
                QPushButton { background-color: #a3be8c; color: #2e3440; font-weight: bold;}
                QPushButton:hover { background-color: #8fbcbb; }
            """)

    def criar_tabela(self, titulo, cor):
        tabela = QTableWidget(0, 4) 
        tabela.setHorizontalHeaderLabels(["ID", "Tipo", "Preço", "Qtd"]) 
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) 
        tabela.setAlternatingRowColors(True)
        tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tabela.setStyleSheet(f"""
            QHeaderView::section {{ 
                background-color: {cor}; 
                color: #2e3440; 
                font-weight: bold; 
                padding: 4px;
                border: none;
            }}
            QTableWidget::item {{
                padding: 4px;
            }}
        """)
        return tabela 

    def atualizar_log(self, texto):
        cursor = self.caixa_log.textCursor() 
        cursor.movePosition(cursor.MoveOperation.End) 
        cursor.insertText(texto) 
        self.caixa_log.setTextCursor(cursor) 
        self.caixa_log.ensureCursorVisible() 

    def adicionar_ordem(self):
        try:
            o_id = int(self.input_id.text()) 
            tipo = 'C' if self.btn_tipo.text() == "Compra" else 'V' 
            preco = float(self.input_preco.text().replace(',', '.')) 
            qtd = int(self.input_qtd.text()) 
            
            nova_ordem = Order(o_id, tipo, preco, qtd) 
            self.fila_entrada.enqueue(nova_ordem) 
            print(f"\n[+] Ordem Enfileirada: {nova_ordem}") 
            if self.clear:
                self.input_id.clear()
                self.input_preco.clear()
                self.input_qtd.clear()
                
            self.input_id.setFocus()

            self.processar_fila() 
        except ValueError: 
            print("[Erro] Entradas inválidas. Verifique os campos de ID, Preço e Quantidade.")

    def processar_fila(self):
        while not self.fila_entrada.is_empty(): 
            ordem = self.fila_entrada.dequeue() 
            if ordem.tipo == 'C': 
                self.livro_compras.insert_ordered(ordem, is_buy_list=True) 
            else: 
                self.livro_vendas.insert_ordered(ordem, is_buy_list=False) 
            
            self.sistema_undo.push(ordem.id) 
            tentar_match(self.livro_compras, self.livro_vendas) 
        
        self.renderizar_tabelas() 

    def desfazer_ordem(self):
        id_cancelar = self.sistema_undo.pop() 
        if id_cancelar is not None: 
            if not self.livro_compras.remove(id_cancelar): 
                self.livro_vendas.remove(id_cancelar) 
            print(f"[Undo] Ordem {id_cancelar} desfeita.") 
            self.renderizar_tabelas() 

    def renderizar_tabelas(self):
        self._preencher_tabela(self.tabela_compras, self.livro_compras) 
        self._preencher_tabela(self.tabela_vendas, self.livro_vendas) 

    def _preencher_tabela(self, tabela, livro):
        tabela.setRowCount(0) 
        atual = livro.head 
        linha = 0 
        while atual: 
            tabela.insertRow(linha) 
            
            def create_item(text, align_right=False):
                item = QTableWidgetItem(text)
                if align_right:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                return item

            tabela.setItem(linha, 0, create_item(str(atual.data.id))) 
            tabela.setItem(linha, 1, create_item(atual.data.tipo)) 
            tabela.setItem(linha, 2, create_item(f"R$ {atual.data.preco:.2f}", align_right=True)) 
            tabela.setItem(linha, 3, create_item(str(atual.data.quantidade), align_right=True)) 
            
            atual = atual.next 
            linha += 1 

    def closeEvent(self, event):
        sys.stdout = sys.__stdout__ 
        super().closeEvent(event) 

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    gui = LivroOfertasPyQt() 
    gui.show() 
    sys.exit(app.exec())
