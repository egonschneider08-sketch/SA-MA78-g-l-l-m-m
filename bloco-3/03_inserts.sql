-- Inserções para a tabela Preco_Sazonal
INSERT INTO Preco_Sazonal (id_preco, id_modulo, id_temporada, valor_sugerido) VALUES
(1, 1, 1, 800.00),
(2, 1, 2, 1200.00),
(3, 1, 4, 1500.00),
(4, 2, 1, 150.00),
(5, 2, 4, 250.00),
(6, 3, 1, 450.00),
(7, 3, 4, 800.00),
(8, 5, 1, 900.00),
(9, 5, 2, 1400.00),
(10, 6, 1, 200.00),
(11, 6, 2, 350.00),
(12, 7, 1, 1500.00),
(13, 7, 4, 2500.00),
(14, 9, 1, 150.00),
(15, 9, 2, 200.00);

-- Inserções para a tabela Cliente
INSERT INTO Cliente (id_cliente, nome, cpf_criptografado, email_criptografado, telefone_criptografado, cep, id_municipio_origem) VALUES
(1, 'João da Silva', 'a1b2c3d4e5', 'hash_email_joao@enc.com', 'hash_tel_1199', '01001-000', 1),
(2, 'Maria Oliveira', 'b2c3d4e5f6', 'hash_email_maria@enc.com', 'hash_tel_2198', '20040-000', 3),
(3, 'Pedro Santos', 'c3d4e5f6g7', 'hash_email_pedro@enc.com', 'hash_tel_4899', '88015-000', 5),
(4, 'Luciana Costa', 'd4e5f6g7h8', 'hash_email_luciana@enc.co', 'hash_tel_7199', '40010-000', 7),
(5, 'Roberto Lima', 'e5f6g7h8i9', 'hash_email_roberto@enc.cc', 'hash_tel_8599', '60060-000', 9),
(6, 'Camila Rocha', 'f6g7h8i9j0', 'hash_email_camila@enc.com', 'hash_tel_1198', '04538-132', 1),
(7, 'Marcos Vinicius', 'g7h8i9j0k1', 'hash_email_marcos@enc.co', 'hash_tel_1999', '13010-111', 2),
(8, 'Aline Mendes', 'h8i9j0k1l2', 'hash_email_aline@enc.com', 'hash_tel_2299', '28950-000', 4),
(9, 'Thiago Borges', 'i9j0k1l2m3', 'hash_email_thiago@enc.com', 'hash_tel_4899', '88330-000', 6),
(10, 'Juliana Paes', 'j0k1l2m3n4', 'hash_email_juliana@enc.com', 'hash_tel_7399', '45810-000', 8),
(11, 'Fernando Nogueira', 'k1l2m3n4o5', 'hash_email_fernando@enc.', 'hash_tel_8598', '62598-000', 10),
(12, 'Patricia Lins', 'l2m3n4o5p6', 'hash_email_patricia@enc.cc', 'hash_tel_1197', '02022-020', 1),
(13, 'Rodrigo Assis', 'm3n4o5p6q7', 'hash_email_rodrigo@enc.cc', 'hash_tel_2197', '22041-010', 3),
(14, 'Carolina Dias', 'n4o5p6q7r8', 'hash_email_carolina@enc.c', 'hash_tel_4898', '88020-100', 5),
(15, 'Eduardo Martins', 'o5p6q7r8s9', 'hash_email_eduardo@enc.c', 'hash_tel_7198', '41810-012', 7);

-- Inserções para a tabela Interesses_Cliente
INSERT INTO Interesses_Cliente (id_interesse, id_cliente, id_municipio_destino, status) VALUES
(1, 1, 4, 'Forte'),
(2, 1, 8, 'Médio'),
(3, 2, 5, 'Forte'),
(4, 3, 10, 'Baixo'),
(5, 4, 1, 'Forte'),
(6, 5, 6, 'Médio'),
(7, 6, 8, 'Forte'),
(8, 7, 4, 'Baixo'),
(9, 8, 1, 'Médio'),
(10, 9, 10, 'Forte'),
(11, 10, 5, 'Médio'),
(12, 11, 3, 'Forte'),
(13, 12, 8, 'Médio'),
(14, 13, 6, 'Baixo'),
(15, 14, 10, 'Forte');

-- Inserções para a tabela Oportunidade_CRM
INSERT INTO Oportunidade_CRM (id_oportunidade, id_cliente, id_usuario_interno, estagio_funil, valor_estimado) VALUES
(1, 1, 1, 'Qualificação', 3500.00),
(2, 2, 2, 'Proposta Enviada', 5200.00),
(3, 3, 1, 'Negociação', 2800.00),
(4, 4, 1, 'Fechado Ganho', 1500.00),
(5, 5, 2, 'Prospecção', 4000.00),
(6, 6, 1, 'Fechado Ganho', 8500.00),
(7, 7, 1, 'Fechado Perdido', 2000.00),
(8, 8, 2, 'Proposta Enviada', 3200.00),
(9, 9, 1, 'Negociação', 6000.00),
(10, 10, 1, 'Fechado Ganho', 4500.00),
(11, 11, 2, 'Qualificação', 2200.00),
(12, 12, 1, 'Prospecção', 5000.00),
(13, 13, 1, 'Fechado Ganho', 3100.00),
(14, 14, 2, 'Negociação', 7200.00),
(15, 15, 1, 'Proposta Enviada', 4800.00);

-- Inserções para a tabela Historico_Interacoes
INSERT INTO Historico_Interacoes (id_interacao, id_oportunidade, id_cliente, id_usuario_interno, tipo_interacao, data_interacao) VALUES
(1, 1, 1, 1, 'Ligação Inicial', '2026-06-21 22:36:06'),
(2, 1, 1, 1, 'Envio de E-mail', '2026-06-21 22:36:06'),
(3, 2, 2, 2, 'Reunião Online', '2026-06-21 22:36:06'),
(4, 2, 2, 2, 'Apresentação de Proposta', '2026-06-21 22:36:06'),
(5, 3, 3, 1, 'Ligação Inicial', '2026-06-21 22:36:06'),
(6, 3, 3, 1, 'Retorno de WhatsApp', '2026-06-21 22:36:06'),
(7, 4, 4, 1, 'Fechamento de Venda', '2026-06-21 22:36:06'),
(8, 5, 5, 2, 'E-mail Frio', '2026-06-21 22:36:06'),
(9, 6, 6, 1, 'Ligação Inicial', '2026-06-21 22:36:06'),
(10, 6, 6, 1, 'Envio de Contrato', '2026-06-21 22:36:06'),
(11, 7, 7, 1, 'Ligação Inicial', '2026-06-21 22:36:06'),
(12, 7, 7, 1, 'Cliente Desistiu - Preço', '2026-06-21 22:36:06'),
(13, 8, 8, 2, 'Reunião Online', '2026-06-21 22:36:06'),
(14, 9, 9, 1, 'Dúvida via WhatsApp', '2026-06-21 22:36:06'),
(15, 10, 10, 1, 'Fechamento de Venda', '2026-06-21 22:36:06'),
(16, 11, 11, 2, 'Ligação Inicial', '2026-06-21 22:36:06'),
(17, 12, 12, 1, 'E-mail de Marketing Aberto', '2026-06-21 22:36:06'),
(18, 13, 13, 1, 'Fechamento de Venda', '2026-06-21 22:36:06'),
(19, 14, 14, 2, 'Envio de Cotação Modificada', '2026-06-21 22:36:06'),
(20, 15, 15, 1, 'Apresentação de Proposta', '2026-06-21 22:36:06');