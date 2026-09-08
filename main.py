import sys
from PyQt6.QtWidgets import QApplication
from app.views.main_window import MainWindow

def main():
    # Inicializa a aplicação
    app = QApplication(sys.argv)
    
    # Cria e exibe a janela principal
    window = MainWindow()
    window.show()
    
    # Executa o loop principal (mantém o programa aberto)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()