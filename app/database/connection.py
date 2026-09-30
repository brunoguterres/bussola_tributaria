import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

if getattr(sys, 'frozen', False):
    caminho_base = sys._MEIPASS
else:
    caminho_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

load_dotenv(os.path.join(caminho_base, '.env'))

def get_connection() -> Client:
    """
    Estabelece e retorna a conexão com o banco de dados Supabase.
    """
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("ERRO: Credenciais do Supabase não encontradas. Verifique o arquivo .env.")
        
    supabase_client: Client = create_client(url, key)
    return supabase_client

if __name__ == "__main__":
    try:
        db = get_connection()
        print("Conexão com o banco de dados estabelecida com sucesso!")
    except Exception as e:
        print(f"Falha ao conectar: {e}")