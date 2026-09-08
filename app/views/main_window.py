from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget
from app.views.formulario import FormularioProduto
from app.views.lista_produtos import ListaProdutos
# IMPORT NOVO: Nosso formulário de regras
from app.views.formulario_regras import FormularioRegras 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Bússola Tributária - Navegação Estratégica IVA")
        self.resize(800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        tabs = QTabWidget()
        
        aba_produtos = FormularioProduto()
        tabs.addTab(aba_produtos, "Cadastro de Produtos")
        
        aba_lista = ListaProdutos()
        tabs.addTab(aba_lista, "Estoque Cadastrado")
        
        # ABA NOVA: Regras Fiscais
        aba_regras = FormularioRegras()
        tabs.addTab(aba_regras, "Regras Fiscais (IVA)")
        
        layout.addWidget(tabs)