-- Carga Inicial de Dimensões
INSERT INTO dim_parceiro (cnpj, razao_social, cnae_principal, uf, regime_tributario) VALUES
('07526557000100', 'AMBEV S.A.', '1113502', 'SP', 'Lucro Real'),
('60409075000152', 'NESTLE BRASIL LTDA.', '1052000', 'SP', 'Lucro Real'),
('61068276000104', 'UNILEVER BRASIL LTDA.', '2021400', 'SP', 'Lucro Real');

INSERT INTO dim_produto (cod_sku, descricao, ncm, tipo_item, imposto_pecado) VALUES
('ALIM-1001', 'Fardo Arroz Branco 5kg', '10063021', 'Revenda', FALSE),
('BEB-2002', 'Cerveja Pilsen Lata 350ml', '22030000', 'Revenda', TRUE);

INSERT INTO dim_regra_fiscal (natureza_operacao, cst_ibs, cst_cbs, aliquota_ibs, aliquota_cbs) VALUES
('Venda Transição 2026', '001', '001', 0.10, 0.90),
('Venda IVA Integral (Projeção)', '001', '001', 17.50, 9.00);
