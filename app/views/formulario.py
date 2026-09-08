from PyQt6.QtWidgets import (QWidget, QFormLayout, QLineEdit, QComboBox, 
                             QCheckBox, QPushButton, QVBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt

class FormularioProduto(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)
        
        # Layout do formulário (alinha Label e Campo automaticamente)
        form_layout = QFormLayout()
        
        # Criando os campos de entrada baseados na nossa tabela Dim_Produto
        self.input_sku = QLineEdit()
        self.input_sku.setPlaceholderText("Ex: PRODUTO-AB0C-001")
        
        self.input_descricao = QLineEdit()
        
        self.input_ncm = QLineEdit()
        self.input_ncm.setMaxLength(8) # O NCM tem no máximo 8 números
        
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Revenda", "Insumo", "Ativo Imobilizado"])
        
        self.check_pecado = QCheckBox("Sujeito ao Imposto Seletivo (Imposto do Pecado)")
        
        # Adicionando os campos ao formulário
        form_layout.addRow("Código SKU:", self.input_sku)
        form_layout.addRow("Descrição:", self.input_descricao)
        form_layout.addRow("Código NCM:", self.input_ncm)
        form_layout.addRow("Tipo de Item:", self.combo_tipo)
        form_layout.addRow("", self.check_pecado) # Deixamos a label vazia para o checkbox ocupar o espaço
        
        # Botão de salvar
        self.btn_salvar = QPushButton("Salvar Produto")
        self.btn_salvar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 8px;")
        
        # Adicionando o formulário e o botão ao layout principal da aba
        layout_principal.addLayout(form_layout)
        layout_principal.addWidget(self.btn_salvar)
        layout_principal.addStretch() # Empurra tudo para cima, não deixando os campos esticados
        
        # Conectando o clique do botão a uma função
        self.btn_salvar.clicked.connect(self.salvar_dados)

    def salvar_dados(self):
        # Por enquanto, apenas vamos pegar os dados da tela para ver se funciona
        sku = self.input_sku.text()
        descricao = self.input_descricao.text()
        ncm = self.input_ncm.text()
        
        if not sku or not descricao or not ncm:
            QMessageBox.warning(self, "Aviso", "Preencha os campos obrigatórios (SKU, Descrição e NCM)!")
            return
            
        QMessageBox.information(self, "Sucesso", f"Produto {sku} lido da tela com sucesso! Em breve enviaremos ao banco.")