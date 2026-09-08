from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget
from app.views.formulario import FormularioProduto
# IMPORT NOVO: Trazendo a nossa lista de produtos
from app.views.lista_produtos import ListaProdutos 

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
        
        # ABA NOVA: Nossa tabela visual
        aba_lista = ListaProdutos()
        tabs.addTab(aba_lista, "Estoque Cadastrado")
        
        layout.addWidget(tabs)