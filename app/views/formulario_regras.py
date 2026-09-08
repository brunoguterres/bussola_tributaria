from PyQt6.QtWidgets import (QWidget, QFormLayout, QLineEdit, QDoubleSpinBox, 
                             QPushButton, QVBoxLayout, QMessageBox)
from app.database.connection import get_connection

class FormularioRegras(QWidget):
    def __init__(self):
        super().__init__()
        
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)
        
        form_layout = QFormLayout()
        
        # Campos de texto
        self.input_natureza = QLineEdit()
        self.input_natureza.setPlaceholderText("Ex: Venda de Produto / Serviço")
        
        self.input_cst_ibs = QLineEdit()
        self.input_cst_ibs.setPlaceholderText("Ex: 001")
        self.input_cst_ibs.setMaxLength(3)
        
        self.input_cst_cbs = QLineEdit()
        self.input_cst_cbs.setPlaceholderText("Ex: 001")
        self.input_cst_cbs.setMaxLength(3)
        
        # Campos de números decimais para as alíquotas
        self.spin_ibs = QDoubleSpinBox()
        self.spin_ibs.setSuffix(" %")
        self.spin_ibs.setDecimals(2) # Duas casas decimais
        self.spin_ibs.setMaximum(100.00) # Limite máximo de 100%
        
        self.spin_cbs = QDoubleSpinBox()
        self.spin_cbs.setSuffix(" %")
        self.spin_cbs.setDecimals(2)
        self.spin_cbs.setMaximum(100.00)
        
        # Montando o layout
        form_layout.addRow("Natureza da Operação:", self.input_natureza)
        form_layout.addRow("CST IBS:", self.input_cst_ibs)
        form_layout.addRow("Alíquota IBS:", self.spin_ibs)
        form_layout.addRow("CST CBS:", self.input_cst_cbs)
        form_layout.addRow("Alíquota CBS:", self.spin_cbs)
        
        self.btn_salvar = QPushButton("Salvar Regra Fiscal")
        self.btn_salvar.setStyleSheet("background-color: #e67e22; color: white; font-weight: bold; padding: 8px;")
        
        layout_principal.addLayout(form_layout)
        layout_principal.addWidget(self.btn_salvar)
        layout_principal.addStretch()
        
        self.btn_salvar.clicked.connect(self.salvar_dados)

    def salvar_dados(self):
        natureza = self.input_natureza.text()
        cst_ibs = self.input_cst_ibs.text()
        cst_cbs = self.input_cst_cbs.text()
        aliquota_ibs = self.spin_ibs.value()
        aliquota_cbs = self.spin_cbs.value()
        
        if not natureza:
            QMessageBox.warning(self, "Aviso", "A Natureza da Operação é obrigatória!")
            return
            
        try:
            db = get_connection()
            
            dados_regra = {
                "natureza_operacao": natureza,
                "cst_ibs": cst_ibs,
                "cst_cbs": cst_cbs,
                "aliquota_ibs": aliquota_ibs,
                "aliquota_cbs": aliquota_cbs
            }
            
            db.table("dim_regra_fiscal").insert(dados_regra).execute()
            
            # Limpa os campos após salvar
            self.input_natureza.clear()
            self.input_cst_ibs.clear()
            self.input_cst_cbs.clear()
            self.spin_ibs.setValue(0.0)
            self.spin_cbs.setValue(0.0)
            
            QMessageBox.information(self, "Sucesso", "Regra fiscal cadastrada com sucesso!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar no banco:\n{str(e)}")