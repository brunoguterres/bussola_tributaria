# Bússola Tributária

**Versão 1.0 · Aplicativo desktop · Python / PyQt6**

O **Bússola Tributária** é uma aplicação desktop de apoio à organização de informações fiscais e à **simulação do IVA Dual brasileiro**, com foco no IBS (Imposto sobre Bens e Serviços) e na CBS (Contribuição sobre Bens e Serviços). A solução reúne cadastros de produtos, parceiros de negócios e regras fiscais em uma interface gráfica, e registra as simulações em um banco de dados Supabase.

> **Escopo:** ferramenta de simulação e apoio à análise. Os parâmetros tributários são cadastrados pelo usuário; o aplicativo não valida automaticamente a legislação aplicável nem substitui orientação contábil ou tributária.

## Funcionalidades

| Módulo | O que faz |
| --- | --- |
| **Cadastro de produtos** | Registra SKU, descrição, NCM, tipo de item (revenda, insumo ou ativo imobilizado) e indicação de sujeição ao Imposto Seletivo. |
| **Estoque cadastrado** | Lista os produtos salvos e permite atualizar a consulta. 
| **Regras fiscais (IVA)** | Cadastra a natureza da operação, os códigos CST e as alíquotas de IBS e CBS. |
| **Cadastro de parceiros** | Registra CNPJ, razão social, CNAE principal, UF e regime tributário (Simples Nacional, Lucro Presumido ou Lucro Real). |
| **Consulta de CNPJ** | Consulta a [BrasilAPI](https://brasilapi.com.br/) para preencher razão social, CNAE e UF a partir do CNPJ informado. |
| **Simulador IVA Dual** | Seleciona produto, parceiro e regra fiscal; calcula base da operação, IBS, CBS e um custo financeiro ilustrativo. |
| **Registro de simulações** | Salva resultados na tabela fato do Supabase, associando produto, parceiro, regra fiscal e data. |

## Tecnologias

- **Python** — linguagem principal da aplicação.
- **PyQt6** — interface gráfica desktop.
- **Supabase** — banco de dados e persistência via cliente Python.
- **Requests** — consultas HTTP à BrasilAPI.
- **python-dotenv** — carregamento de configurações locais por variáveis de ambiente.
- **Pandas** — incluído no `requirements.txt`.
- **PyInstaller** — formato compatível com a distribuição executável analisada; não inclui um script de build ou arquivo `.spec` para reproduzi-la.

O arquivo `requirements.txt` define `PyQt6==6.7.0`, `requests==2.31.0`, `python-dotenv==1.0.1`, `supabase` e `pandas`. 

## Estrutura do projeto

```text
bussola_tributaria-1.0/
├── main.py                         # Inicialização da aplicação
├── requirements.txt                # Dependências Python
├── .gitignore                      # Regras de exclusão do Git
└── app/
    ├── database/
    │   └── connection.py           # Conexão com Supabase
    ├── etl/
    │   └── receita_api.py          # Consulta de CNPJ na BrasilAPI
    └── views/
        ├── main_window.py          # Janela principal e abas
        ├── formulario.py           # Cadastro de produtos
        ├── lista_produtos.py       # Listagem de produtos
        ├── formulario_regras.py    # Cadastro de regras fiscais
        ├── formulario_parceiros.py # Cadastro de parceiros
        └── simulador.py            # Simulação tributária e registros
```

Os pacotes `bussola_tributaria-1.0.zip` e `bussola_tributaria-1.0.tar.gz` apresentam a mesma estrutura de código-fonte. O arquivo `bussola_tributaria_v1_0.zip` contém uma distribuição executável para Windows, com `main/main.exe` e a pasta de dependências `main/_internal/`.

## Instalação pelo código-fonte

**Pré-requisitos:** Python e `pip`, acesso à internet para instalar dependências e consultar a BrasilAPI, além de um projeto Supabase configurado. Para maior compatibilidade, comece com um ambiente Python compatível com as versões fixadas em `requirements.txt` e verifique a instalação das bibliotecas.

1. Extraia `bussola_tributaria-1.0.zip` (ou `bussola_tributaria-1.0.tar.gz`) e abra um terminal na pasta que contém `main.py`.
2. Crie um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

3. Ative o ambiente virtual:

   **Windows (PowerShell):**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **Linux / macOS:**

   ```bash
   source .venv/bin/activate
   ```

4. Instale as dependências:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Configure as variáveis de ambiente conforme a próxima seção.
6. Execute a aplicação:

   ```bash
   python main.py
   ```


## Configuração do Supabase

A aplicação lê duas variáveis de um arquivo `.env` na raiz do projeto:

```dotenv
SUPABASE_URL=https://SEU-PROJETO.supabase.co
SUPABASE_KEY=SUA_CHAVE_DE_ACESSO
```


### Tabelas utilizadas

O código pressupõe a existência das tabelas abaixo no Supabase:

| Tabela | Campos usados no código |
| --- | --- |
| `dim_produto` | `sk_produto`, `cod_sku`, `descricao`, `ncm`, `tipo_item`, `imposto_pecado` |
| `dim_parceiro` | `sk_parceiro`, `cnpj`, `razao_social`, `cnae_principal`, `uf`, `regime_tributario` |
| `dim_regra_fiscal` | `sk_regra`, `natureza_operacao`, `cst_ibs`, `cst_cbs`, `aliquota_ibs`, `aliquota_cbs` |
| `dim_tempo` | `sk_tempo`, `data_completa`, `ano`, `mes`, `trimestre` |
| `fato_movimento_fiscal` | `sk_tempo`, `sk_produto`, `sk_parceiro`, `sk_regra`, `numero_nfe`, `quantidade`, `valor_liquido`, `base_calculo_ibs`, `valor_ibs`, `base_calculo_cbs`, `valor_cbs`, `custo_perda_float` |

**Atenção:** esta é uma relação dos campos acessados pelo código, **não** um esquema SQL completo. Tipos, chaves, relacionamentos, restrições e políticas RLS precisam ser definidos no banco.

## Como utilizar

1. Na aba **Cadastro de Produtos**, informe SKU, descrição, NCM e classificação do item.
2. Consulte os produtos na aba **Estoque Cadastrado**.
3. Na aba **Regras Fiscais (IVA)**, cadastre a natureza de operação, CST e alíquotas de IBS/CBS.
4. Em **Cadastro de Parceiros**, informe o CNPJ e, se desejar, use **Buscar CNPJ na API** para preencher os dados disponíveis; selecione o regime tributário e salve.
5. Abra **Simulador IVA Dual (Fato)**, clique em **Sincronizar Cadastros**, selecione produto, parceiro e regra, e informe quantidade e valor unitário líquido.
6. Clique em **Simular Impacto Tributário**. Para persistir os dados, use **Registrar Operação na Fato**.

### Lógica do simulador

A implementação atual aplica os seguintes cálculos:

```text
base_calculo = quantidade × valor_unitario_liquido
valor_ibs = base_calculo × (aliquota_ibs / 100)
valor_cbs = base_calculo × (aliquota_cbs / 100)
imposto_total = valor_ibs + valor_cbs
custo_perda_float = imposto_total × 0,015
```


## Executável para Windows

O pacote `bussola_tributaria_v1_0.zip` contém uma versão empacotada para Windows de 64 bits:

```text
main/
├── main.exe
└── _internal/
    └── ... dependências e bibliotecas ...
```

Para abrir, extraia integralmente o ZIP e execute `main/main.exe`. **Não separe** o executável da pasta `_internal`. O pacote inclui componentes da execução Python, dispensando a instalação manual de Python para essa modalidade.


> **Segurança:** o ZIP do executável analisado inclui `main/_internal/.env`. Remova credenciais privadas e revise a estratégia de distribuição **antes** de publicar o pacote. Remover o arquivo sem estabelecer outra forma de configuração pode impedir a conexão com o banco de dados.


## Entregas Técnicas - Segunda Etapa (TBD)

Para atender aos critérios de avaliação da disciplina, os seguintes artefatos e evidências foram incluídos no repositório:

* **Script DDL:** Localizado no diretório `DDL/` (arquivo `ddl_criacao_tabelas.sql`). Contém a criação da modelagem dimensional (Star Schema) e da Tabela Fato.
* **Script DML:** Localizado no diretório `DML/` (arquivo `dml_carga_dados.sql`). Contém a carga inicial de dados para as dimensões.
* **Operações OLAP:** Localizadas na pasta raiz as imagens com prefixo `OLAP_*` de *queries* analíticas executadas no Supabase demonstrando as agregações de impacto financeiro segmentadas por fornecedor e incidência de imposto do pecado.
* **Fonte de Extração (ETL):** O processo de extração, transformação e carga é realizado via integração em tempo real com a [BrasilAPI](https://brasilapi.com.br/) (código fonte em `app/etl/receita_api.py`), garantindo dados cadastrais validados de CNPJs.
* **Vídeo Demonstrativo:** [Inserir o Link do Vídeo Aqui]

---

**Bússola Tributária — versão 1.0**
