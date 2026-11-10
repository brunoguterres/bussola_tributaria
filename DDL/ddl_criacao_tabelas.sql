-- Criação das Tabelas de Dimensão
CREATE TABLE dim_produto (
    sk_produto SERIAL PRIMARY KEY,
    cod_sku VARCHAR(50),
    descricao VARCHAR(255),
    ncm VARCHAR(20),
    tipo_item VARCHAR(50),
    imposto_pecado BOOLEAN
);

CREATE TABLE dim_parceiro (
    sk_parceiro SERIAL PRIMARY KEY,
    cnpj VARCHAR(14),
    razao_social VARCHAR(255),
    cnae_principal VARCHAR(20),
    uf VARCHAR(2),
    regime_tributario VARCHAR(50)
);

CREATE TABLE dim_regra_fiscal (
    sk_regra SERIAL PRIMARY KEY,
    natureza_operacao VARCHAR(255),
    cst_ibs VARCHAR(10),
    cst_cbs VARCHAR(10),
    aliquota_ibs DECIMAL(5,2),
    aliquota_cbs DECIMAL(5,2)
);

CREATE TABLE dim_tempo (
    sk_tempo INTEGER PRIMARY KEY,
    data_completa DATE,
    ano INTEGER,
    mes INTEGER,
    trimestre INTEGER
);

-- Criação da Tabela Fato
CREATE TABLE fato_movimento_fiscal (
    id SERIAL PRIMARY KEY,
    sk_tempo INTEGER REFERENCES dim_tempo(sk_tempo),
    sk_produto INTEGER REFERENCES dim_produto(sk_produto),
    sk_parceiro INTEGER REFERENCES dim_parceiro(sk_parceiro),
    sk_regra INTEGER REFERENCES dim_regra_fiscal(sk_regra),
    numero_nfe VARCHAR(50),
    quantidade DECIMAL(10,2),
    valor_liquido DECIMAL(15,2),
    base_calculo_ibs DECIMAL(15,2),
    valor_ibs DECIMAL(15,2),
    base_calculo_cbs DECIMAL(15,2),
    valor_cbs DECIMAL(15,2),
    custo_perda_float DECIMAL(15,2)
);
