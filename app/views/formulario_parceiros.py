from PyQt6.QtWidgets import (QWidget, QFormLayout, QLineEdit, QComboBox, 
                             QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout)
from app.database.connection import get_connection
from app.etl.receita_api import buscar_dados_cnpj 

class FormularioParceiros(QWidget):
    def __init__(self):
        super().__init__()
        
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)
        form_layout = QFormLayout()
        
        layout_cnpj = QHBoxLayout()
        self.input_cnpj = QLineEdit()
        self.input_cnpj.setPlaceholderText("Apenas números (Ex: 34028316000103)")
        
        self.btn_buscar = QPushButton("Buscar CNPJ na API")
        self.btn_buscar.setStyleSheet("background-color: #8e44ad; color: white; font-weight: bold;")
        self.btn_buscar.clicked.connect(self.buscar_dados_api)
        
        layout_cnpj.addWidget(self.input_cnpj)
        layout_cnpj.addWidget(self.btn_buscar)
        
        self.input_razao = QLineEdit()
        self.input_cnae = QLineEdit()
        
        self.input_uf = QLineEdit()
        self.input_uf.setMaxLength(2)
        
        self.combo_regime = QComboBox()
        self.combo_regime.addItems(["Simples Nacional", "Lucro Presumido", "Lucro Real"])
        
        form_layout.addRow("CNPJ:", layout_cnpj)
        form_layout.addRow("Razão Social:", self.input_razao)
        form_layout.addRow("CNAE Principal:", self.input_cnae)
        form_layout.addRow("Estado (UF):", self.input_uf)
        form_layout.addRow("Regime Tributário:", self.combo_regime)
        
        self.btn_guardar = QPushButton("Guardar Parceiro")
        self.btn_guardar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 8px;")
        self.btn_guardar.clicked.connect(self.guardar_dados)
        
        layout_principal.addLayout(form_layout)
        layout_principal.addWidget(self.btn_guardar)
        layout_principal.addStretch()

    def buscar_dados_api(self):
        cnpj = self.input_cnpj.text()
        if not cnpj:
            QMessageBox.warning(self, "Aviso", "Digite um CNPJ para buscar.")
            return
            
        try:
            dados = buscar_dados_cnpj(cnpj)
            
            self.input_razao.setText(dados.get("razao_social", ""))
            self.input_cnae.setText(dados.get("cnae_principal", ""))
            self.input_uf.setText(dados.get("uf", ""))
            
            QMessageBox.information(self, "Sucesso", "Dados extraídos da Receita Federal com sucesso!")
        except Exception as e:
            QMessageBox.warning(self, "Erro na Busca", str(e))

    def guardar_dados(self):
        cnpj = self.input_cnpj.text()
        razao = self.input_razao.text()
        
        if not cnpj or not razao:
            QMessageBox.warning(self, "Aviso", "Os campos CNPJ e Razão Social são obrigatórios!")
            return
            
        try:
            db = get_connection()
            
            dados_parceiro = {
                "cnpj": cnpj.replace(".", "").replace("/", "").replace("-", "").strip(),
                "razao_social": razao,
                "cnae_principal": self.input_cnae.text(),
                "uf": self.input_uf.text(),
                "regime_tributario": self.combo_regime.currentText()
            }
            
            db.table("dim_parceiro").insert(dados_parceiro).execute()
            
            self.input_cnpj.clear()
            self.input_razao.clear()
            self.input_cnae.clear()
            self.input_uf.clear()
            
            QMessageBox.information(self, "Sucesso", "Parceiro de negócio registado com sucesso!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao guardar na base de dados:\n{str(e)}")