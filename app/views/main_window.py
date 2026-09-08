from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurações básicas da janela
        self.setWindowTitle("Bússola Tributária - Navegação Estratégica IVA")
        self.resize(800, 600)
        
        # Widget central e Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Um texto de boas-vindas simples para testarmos
        titulo = QLabel("Bem-vindo ao Bússola Tributária")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Estilização simples usando CSS (QSS)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50;")
        
        layout.addWidget(titulo)