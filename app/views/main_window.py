from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget
from app.views.formulario import FormularioProduto # Importamos nosso formulário aqui

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Bússola Tributária - Navegação Estratégica IVA")
        self.resize(800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Vamos usar um sistema de Abas (Tabs) para organizar o sistema
        tabs = QTabWidget()
        
        # Aba 1: O nosso formulário de produto
        aba_produtos = FormularioProduto()
        tabs.addTab(aba_produtos, "Cadastro de Produtos")
        
        # Aba 2: Deixando um espaço para as Regras Fiscais depois
        aba_regras = QWidget()
        tabs.addTab(aba_regras, "Regras Fiscais (Em breve)")
        
        layout.addWidget(tabs)