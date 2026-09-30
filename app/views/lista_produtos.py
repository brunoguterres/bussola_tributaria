from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QMessageBox, QHeaderView)
from app.database.connection import get_connection

class ListaProdutos(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.btn_atualizar = QPushButton("Atualizar Dados")
        self.btn_atualizar.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 8px;")
        self.btn_atualizar.clicked.connect(self.carregar_dados)
        
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(["SKU", "Descrição", "NCM", "Tipo", "Imposto do Pecado"])
        
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.btn_atualizar)
        layout.addWidget(self.tabela)
        
        self.carregar_dados()

    def carregar_dados(self):
        try:
            db = get_connection()
            
            resposta = db.table("dim_produto").select("*").execute()
            dados = resposta.data
            
            self.tabela.setRowCount(len(dados))
            
            for linha_idx, produto in enumerate(dados):
                self.tabela.setItem(linha_idx, 0, QTableWidgetItem(produto.get("cod_sku", "")))
                self.tabela.setItem(linha_idx, 1, QTableWidgetItem(produto.get("descricao", "")))
                self.tabela.setItem(linha_idx, 2, QTableWidgetItem(produto.get("ncm", "")))
                self.tabela.setItem(linha_idx, 3, QTableWidgetItem(produto.get("tipo_item", "")))
                
                texto_pecado = "Sim" if produto.get("imposto_pecado") else "Não"
                self.tabela.setItem(linha_idx, 4, QTableWidgetItem(texto_pecado))
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar os dados:\n{str(e)}")