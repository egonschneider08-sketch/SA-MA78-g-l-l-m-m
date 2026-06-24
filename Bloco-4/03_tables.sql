CREATE TABLE Solicitacao_SLA (
    id_solicitacao INT AUTO_INCREMENT PRIMARY KEY,
    id_oportunidade INT NOT NULL,
    id_parceiro INT NOT NULL,
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_oportunidade) REFERENCES Oportunidade_CRM(id_oportunidade),
    FOREIGN KEY (id_parceiro) REFERENCES Parceiros(id_parceiro)
);

CREATE TABLE Cotacao_Personalizadas (
    id_cotacao INT AUTO_INCREMENT PRIMARY KEY,
    id_oportunidade INT NOT NULL,
    id_pacote INT,
    valor_total_calculado DECIMAL(10, 2),
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_oportunidade) REFERENCES Oportunidade_CRM(id_oportunidade),
    FOREIGN KEY (id_pacote) REFERENCES Pacote(id_pacote)
);

CREATE TABLE Item_Cotacao (
    id_item_cotacao INT AUTO_INCREMENT PRIMARY KEY,
    id_cotacao INT NOT NULL,
    id_modulo INT NOT NULL,
    valor_aplicado DECIMAL(10, 2) NOT NULL,
    UNIQUE (id_cotacao, id_modulo),
    FOREIGN KEY (id_cotacao) REFERENCES Cotacao_Personalizadas(id_cotacao),
    FOREIGN KEY (id_modulo) REFERENCES Modulos_Pacote(id_modulo)
);