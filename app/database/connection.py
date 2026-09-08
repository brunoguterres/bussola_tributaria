import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def get_connection() -> Client:
    """
    Estabelece e retorna a conexão com o banco de dados Supabase.
    """
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("ERRO: Credenciais do Supabase não encontradas. Verifique o arquivo .env.")

    # Cria a instância do cliente conectando ao PostgreSQL do Supabase
    supabase_client: Client = create_client(url, key)
    return supabase_client

# Teste rápido de conexão (só roda se você executar este arquivo diretamente)
if __name__ == "__main__":
    try:
        db = get_connection()
        print("Conexão com o banco de dados estabelecida com sucesso!")
    except Exception as e:
        print(f"Falha ao conectar: {e}")