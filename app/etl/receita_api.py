import requests

def buscar_dados_cnpj(cnpj: str) -> dict:
    """
    Busca os dados de uma empresa na BrasilAPI utilizando o CNPJ.
    Retorna um dicionário com Razão Social, CNAE e UF.
    """
    # Higienização dos dados: remove pontos, barras e traços
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
    
    if len(cnpj_limpo) != 14:
        raise ValueError("O CNPJ deve conter exatamente 14 números.")
        
    # Faz a requisição na API pública
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
    
    try:
        resposta = requests.get(url, timeout=10)
        
        # Verifica se a busca deu certo (Status 200 = OK)
        if resposta.status_code == 200:
            dados = resposta.json()
            
            # Retorna apenas o que precisamos para a tabela Dim_Parceiro
            return {
                "cnpj": cnpj_limpo,
                "razao_social": dados.get("razao_social", ""),
                "cnae_principal": str(dados.get("cnae_fiscal", "")),
                "uf": dados.get("uf", "")
            }
        else:
            raise Exception("CNPJ não encontrado na base de dados.")
            
    except requests.exceptions.RequestException:
        raise Exception("Falha de conexão. Verifique a sua internet.")