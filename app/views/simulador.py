from PyQt6.QtWidgets import (QWidget, QFormLayout, QComboBox, QDoubleSpinBox, 
                             QPushButton, QVBoxLayout, QMessageBox, QLabel, QGroupBox)
from PyQt6.QtCore import Qt
from app.database.connection import get_connection
from datetime import datetime

class SimuladorTributario(QWidget):
    def __init__(self):
        super().__init__()
        
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)
        
        grupo_entradas = QGroupBox("1. Seleção de Parâmetros")
        form_entradas = QFormLayout()
        
        self.combo_produto = QComboBox()
        self.combo_parceiro = QComboBox()
        self.combo_regra = QComboBox()

        self.btn_atualizar = QPushButton("↻ Sincronizar Cadastros")
        self.btn_atualizar.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold; padding: 5px;")
        self.btn_atualizar.clicked.connect(self.carregar_dados_combos)
        
        self.spin_quantidade = QDoubleSpinBox()
        self.spin_quantidade.setDecimals(2)
        self.spin_quantidade.setMaximum(999999.99)
        self.spin_quantidade.setValue(1.0)
        
        self.spin_valor_unitario = QDoubleSpinBox()
        self.spin_valor_unitario.setPrefix("R$ ")
        self.spin_valor_unitario.setDecimals(2)
        self.spin_valor_unitario.setMaximum(9999999.99)

        form_entradas.addRow("", self.btn_atualizar)
        form_entradas.addRow("Produto:", self.combo_produto)
        form_entradas.addRow("Parceiro de Negócio:", self.combo_parceiro)
        form_entradas.addRow("Regra Fiscal:", self.combo_regra)
        form_entradas.addRow("Quantidade:", self.spin_quantidade)
        form_entradas.addRow("Valor Unitário Líquido:", self.spin_valor_unitario)
        
        grupo_entradas.setLayout(form_entradas)
        layout_principal.addWidget(grupo_entradas)
        
        grupo_resultados = QGroupBox("2. Análise de Impacto (IVA Dual)")
        form_resultados = QFormLayout()
        
        self.lbl_valor_total = QLabel("R$ 0.00")
        self.lbl_valor_ibs = QLabel("R$ 0.00")
        self.lbl_valor_cbs = QLabel("R$ 0.00")
        self.lbl_perda_float = QLabel("R$ 0.00")
        
        estilo_destaque = "font-weight: bold; color: #c0392b; font-size: 14px;"
        self.lbl_valor_ibs.setStyleSheet(estilo_destaque)
        self.lbl_valor_cbs.setStyleSheet(estilo_destaque)
        self.lbl_perda_float.setStyleSheet("font-weight: bold; color: #d35400; font-size: 14px;")
        
        form_resultados.addRow("Valor Total da Base:", self.lbl_valor_total)
        form_resultados.addRow("Impacto IBS:", self.lbl_valor_ibs)
        form_resultados.addRow("Impacto CBS:", self.lbl_valor_cbs)
        form_resultados.addRow("Custo de Secagem do Caixa (Split Payment):", self.lbl_perda_float)
        
        grupo_resultados.setLayout(form_resultados)
        layout_principal.addWidget(grupo_resultados)
        
        self.btn_calcular = QPushButton("Simular Impacto Tributário")
        self.btn_calcular.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 10px;")
        self.btn_calcular.clicked.connect(self.calcular_impostos)
        
        self.btn_salvar = QPushButton("Registrar Operação na Fato")
        self.btn_salvar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 10px;")
        self.btn_salvar.clicked.connect(self.salvar_movimento)
        
        layout_principal.addWidget(self.btn_calcular)
        layout_principal.addWidget(self.btn_salvar)
        layout_principal.addStretch()
        
        self.calculo_atual = {}
        
        self.carregar_dados_combos()

    def carregar_dados_combos(self):
        """Busca os dados do Supabase e preenche as caixas de seleção."""

        self.combo_produto.clear()
        self.combo_parceiro.clear()
        self.combo_regra.clear()

        try:
            db = get_connection()
            
            produtos = db.table("dim_produto").select("sk_produto, descricao").execute().data
            for p in produtos:
                self.combo_produto.addItem(p["descricao"], userData=p["sk_produto"])
            
            parceiros = db.table("dim_parceiro").select("sk_parceiro, razao_social").execute().data
            for p in parceiros:
                self.combo_parceiro.addItem(p["razao_social"], userData=p["sk_parceiro"])
            
            regras = db.table("dim_regra_fiscal").select("*").execute().data
            for r in regras:
                texto = f"{r['natureza_operacao']} (IBS: {r['aliquota_ibs']}% | CBS: {r['aliquota_cbs']}%)"
                self.combo_regra.addItem(texto, userData=r)
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Não foi possível carregar os cadastros.\n{str(e)}")

    def calcular_impostos(self):
        """Realiza a matemática do IVA Dual e atualiza a interface."""
        if self.combo_regra.currentData() is None:
            QMessageBox.warning(self, "Aviso", "Selecione uma regra fiscal válida.")
            return

        regra = self.combo_regra.currentData()
        qtd = self.spin_quantidade.value()
        valor_un = self.spin_valor_unitario.value()
        
        base_calculo = qtd * valor_un
        valor_ibs = base_calculo * (float(regra["aliquota_ibs"]) / 100)
        valor_cbs = base_calculo * (float(regra["aliquota_cbs"]) / 100)
        
        imposto_total = valor_ibs + valor_cbs
        custo_float = imposto_total * 0.015 
        
        self.lbl_valor_total.setText(f"R$ {base_calculo:.2f}")
        self.lbl_valor_ibs.setText(f"R$ {valor_ibs:.2f}")
        self.lbl_valor_cbs.setText(f"R$ {valor_cbs:.2f}")
        self.lbl_perda_float.setText(f"R$ {custo_float:.2f}")
        
        self.calculo_atual = {
            "sk_produto": self.combo_produto.currentData(),
            "sk_parceiro": self.combo_parceiro.currentData(),
            "sk_regra": regra["sk_regra"],
            "quantidade": qtd,
            "valor_liquido": base_calculo,
            "base_calculo_ibs": base_calculo,
            "valor_ibs": valor_ibs,
            "base_calculo_cbs": base_calculo,
            "valor_cbs": valor_cbs,
            "custo_perda_float": custo_float
        }

    def garantir_dim_tempo(self, db):
        """Verifica se o dia de hoje existe na Dim_Tempo, se não, insere."""
        hoje = datetime.now()
        sk_tempo = int(hoje.strftime("%Y%m%d"))
        
        existe = db.table("dim_tempo").select("sk_tempo").eq("sk_tempo", sk_tempo).execute().data
        if not existe:
            db.table("dim_tempo").insert({
                "sk_tempo": sk_tempo,
                "data_completa": hoje.strftime("%Y-%m-%d"),
                "ano": hoje.year,
                "mes": hoje.month,
                "trimestre": (hoje.month - 1) // 3 + 1
            }).execute()
            
        return sk_tempo

    def salvar_movimento(self):
        """Salva a operação na Tabela Fato."""
        if not self.calculo_atual:
            QMessageBox.warning(self, "Aviso", "Calcule os impostos antes de salvar.")
            return
            
        try:
            db = get_connection()
            sk_tempo = self.garantir_dim_tempo(db)
            
            dados_fato = self.calculo_atual.copy()
            dados_fato["sk_tempo"] = sk_tempo
            dados_fato["numero_nfe"] = f"NFE-SIMULACAO-{datetime.now().strftime('%H%M%S')}"
            
            db.table("fato_movimento_fiscal").insert(dados_fato).execute()
            
            QMessageBox.information(self, "Sucesso", "Operação registrada na Fato com sucesso!")
            self.calculo_atual.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar operação:\n{str(e)}")