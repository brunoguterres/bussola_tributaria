from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QMessageBox, QHeaderView)
from app.database.connection import get_connection

class ListaProdutos(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 1. Criando o botão de atualizar
        self.btn_atualizar = QPushButton("Atualizar Dados")
        self.btn_atualizar.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 8px;")
        self.btn_atualizar.clicked.connect(self.carregar_dados)
        
        # 2. Criando a tabela visual
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(["SKU", "Descrição", "NCM", "Tipo", "Imposto do Pecado"])
        
        # Faz as colunas se esticarem para preencher o espaço da tela
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.btn_atualizar)
        layout.addWidget(self.tabela)
        
        # Carrega os dados automaticamente ao abrir a tela
        self.carregar_dados()

    def carregar_dados(self):
        try:
            db = get_connection()
            
            # Busca todos os registros da tabela dim_produto
            resposta = db.table("dim_produto").select("*").execute()
            dados = resposta.data
            
            # Configura o número de linhas da tabela visual com base no que veio do banco
            self.tabela.setRowCount(len(dados))
            
            # Preenche a tabela linha por linha
            for linha_idx, produto in enumerate(dados):
                self.tabela.setItem(linha_idx, 0, QTableWidgetItem(produto.get("cod_sku", "")))
                self.tabela.setItem(linha_idx, 1, QTableWidgetItem(produto.get("descricao", "")))
                self.tabela.setItem(linha_idx, 2, QTableWidgetItem(produto.get("ncm", "")))
                self.tabela.setItem(linha_idx, 3, QTableWidgetItem(produto.get("tipo_item", "")))
                
                # Transforma o True/False do banco em Sim/Não para ficar mais amigável
                texto_pecado = "Sim" if produto.get("imposto_pecado") else "Não"
                self.tabela.setItem(linha_idx, 4, QTableWidgetItem(texto_pecado))
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar os dados:\n{str(e)}")