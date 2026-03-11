CREATE DATABASE IF NOT EXISTS caobalhota;
USE caobalhota;

-- 1. Tabela CLIENTE
CREATE TABLE CLIENTagendamentoE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    endereco VARCHAR(255)
);

-- 2. Tabela FUNCIONARIO
CREATE TABLE FUNCIONARIO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50),
    telefone VARCHAR(20),
    email VARCHAR(100),
    login VARCHAR(50) UNIQUE,
    senha VARCHAR(255) 
);

-- 3. Tabela SERVICO
CREATE TABLE SERVICO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    valor_base DOUBLE NOT NULL,
    descricao TEXT
);

-- 4. Tabela PRODUTO
CREATE TABLE PRODUTO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50),
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DOUBLE NOT NULL,
    estoque INT DEFAULT 0
);

-- 5. Tabela PET (Depende de CLIENTE)
CREATE TABLE PET (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    nome VARCHAR(100) NOT NULL,
    tipo ENUM('cão', 'gato'),
    raca VARCHAR(50),
    porte ENUM('pequeno', 'médio', 'grande'),
    cuidados_especiais TEXT,
    CONSTRAINT fk_pet_cliente FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id)
);

-- 6. Tabela VENDA (Depende de CLIENTE)
CREATE TABLE VENDA (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    data_venda DATE,
    valor_total DOUBLE,
    CONSTRAINT fk_venda_cliente FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id)
);

-- 7. Tabela AGENDAMENTO (Depende de várias)
CREATE TABLE AGENDAMENTO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_pet INT,
    id_servico INT,
    id_funcionario INT,
    data DATE,
    hora TIME,
    status ENUM('agendado', 'iniciado', 'concluído', 'cancelado', 'pago'),
    cor_tintura VARCHAR(30),
    observacoes TEXT,
    CONSTRAINT fk_age_cliente FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id),
    CONSTRAINT fk_age_pet FOREIGN KEY (id_pet) REFERENCES PET(id),
    CONSTRAINT fk_age_servico FOREIGN KEY (id_servico) REFERENCES SERVICO(id),
    CONSTRAINT fk_age_func FOREIGN KEY (id_funcionario) REFERENCES FUNCIONARIO(id)
);

-- 8. Tabela ITEM_VENDA (Depende de VENDA, PRODUTO e SERVICO)
CREATE TABLE ITEM_VENDA (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_venda INT,
    id_produto INT NULL,
    id_servico INT NULL,
    quantidade INT,
    valor_unitario DOUBLE,
    tipo_item ENUM('produto', 'servico'),
    CONSTRAINT fk_item_venda FOREIGN KEY (id_venda) REFERENCES VENDA(id),
    CONSTRAINT fk_item_prod FOREIGN KEY (id_produto) REFERENCES PRODUTO(id),
    CONSTRAINT fk_item_serv FOREIGN KEY (id_servico) REFERENCES SERVICO(id)
);