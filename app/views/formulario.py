from PyQt6.QtWidgets import (QWidget, QFormLayout, QLineEdit, QComboBox, 
                             QCheckBox, QPushButton, QVBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt

# IMPORT NOVO: Trazendo a nossa conexão com o Supabase
from app.database.connection import get_connection

class FormularioProduto(QWidget):
    def __init__(self):
        super().__init__()
        
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)
        
        form_layout = QFormLayout()
        
        self.input_sku = QLineEdit()
        self.input_sku.setPlaceholderText("Ex: PRODUTO-AB9C-001")
        
        self.input_descricao = QLineEdit()
        
        self.input_ncm = QLineEdit()
        self.input_ncm.setMaxLength(8)
        
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Revenda", "Insumo", "Ativo Imobilizado"])
        
        self.check_pecado = QCheckBox("Sujeito ao Imposto Seletivo (Imposto do Pecado)")
        
        form_layout.addRow("Código SKU:", self.input_sku)
        form_layout.addRow("Descrição:", self.input_descricao)
        form_layout.addRow("Código NCM:", self.input_ncm)
        form_layout.addRow("Tipo de Item:", self.combo_tipo)
        form_layout.addRow("", self.check_pecado)
        
        self.btn_salvar = QPushButton("Salvar Produto")
        self.btn_salvar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 8px;")
        
        layout_principal.addLayout(form_layout)
        layout_principal.addWidget(self.btn_salvar)
        layout_principal.addStretch()
        
        self.btn_salvar.clicked.connect(self.salvar_dados)

    def salvar_dados(self):
        # 1. Pegamos os dados da tela
        sku = self.input_sku.text()
        descricao = self.input_descricao.text()
        ncm = self.input_ncm.text()
        tipo = self.combo_tipo.currentText()
        pecado = self.check_pecado.isChecked()
        
        if not sku or not descricao or not ncm:
            QMessageBox.warning(self, "Aviso", "Preencha os campos obrigatórios (SKU, Descrição e NCM)!")
            return
            
        try:
            # 2. Conectamos ao banco de dados
            db = get_connection()
            
            # 3. Montamos o "pacote" de dados (dicionário) com os nomes exatos das colunas do banco
            dados_produto = {
                "cod_sku": sku,
                "descricao": descricao,
                "ncm": ncm,
                "tipo_item": tipo,
                "imposto_pecado": pecado
            }
            
            # 4. Enviamos para a tabela dim_produto
            db.table("dim_produto").insert(dados_produto).execute()
            
            # 5. Limpamos a tela para o próximo cadastro
            self.input_sku.clear()
            self.input_descricao.clear()
            self.input_ncm.clear()
            self.check_pecado.setChecked(False)
            
            QMessageBox.information(self, "Sucesso", f"Produto '{descricao}' salvo no banco de dados!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar no banco:\n{str(e)}")