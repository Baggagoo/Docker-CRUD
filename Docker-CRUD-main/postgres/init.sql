-- Script para inicializar o banco de dados "escola"

-- Criar o banco de dados
--CREATE DATABASE escola;

-- Conectar ao banco de dados "escola"
--\c escola;

-- Criar a tabela "alunos"
CREATE TABLE alunos (
    aluno_id CHARACTER VARYING(5) NOT NULL,
    nome CHARACTER VARYING(40) NOT NULL,
    endereco CHARACTER VARYING(60),
    cidade CHARACTER VARYING(15),
    estado CHARACTER VARYING(15),
    cep CHARACTER VARYING(10),
    pais CHARACTER VARYING(15),
    telefone CHARACTER VARYING(24),
    PRIMARY KEY (aluno_id)
);

-- Criar a tabela "professores"
CREATE TABLE professores (
    professor_id CHARACTER VARYING(5) NOT NULL,
    nome CHARACTER VARYING(40) NOT NULL,
    departamento CHARACTER VARYING(40),
    email CHARACTER VARYING(60),
    telefone CHARACTER VARYING(24),
    PRIMARY KEY (professor_id)
);

-- Criar a tabela "pagamentos"
CREATE TABLE pagamentos (
    pagamento_id SERIAL PRIMARY KEY,
    aluno_id CHARACTER VARYING(5) NOT NULL,
    valor NUMERIC(10, 2) NOT NULL,
    data_pagamento DATE NOT NULL,
    metodo_pagamento CHARACTER VARYING(20),
    FOREIGN KEY (aluno_id) REFERENCES alunos (aluno_id)
);

-- Criar a tabela "presencas"
CREATE TABLE presencas (
    presenca_id SERIAL PRIMARY KEY,
    aluno_id CHARACTER VARYING(5) NOT NULL,
    data DATE NOT NULL,
    status CHARACTER VARYING(10) NOT NULL,
    FOREIGN KEY (aluno_id) REFERENCES alunos (aluno_id)
);

-- Criar a tabela "atividades"
CREATE TABLE atividades (
    atividade_id SERIAL PRIMARY KEY,
    titulo CHARACTER VARYING(100) NOT NULL,
    descricao TEXT,
    data_entrega DATE NOT NULL
);

-- Criar a tabela "atividades_alunos"
CREATE TABLE atividades_alunos (
    atividade_aluno_id SERIAL PRIMARY KEY,
    atividade_id INT NOT NULL,
    aluno_id CHARACTER VARYING(5) NOT NULL,
    status CHARACTER VARYING(20),
    nota NUMERIC(5, 2),
    FOREIGN KEY (atividade_id) REFERENCES atividades (atividade_id),
    FOREIGN KEY (aluno_id) REFERENCES alunos (aluno_id)
);

-- Criar a tabela "usuarios"
CREATE TABLE usuarios (
    usuario_id SERIAL PRIMARY KEY,
    nome CHARACTER VARYING(50) NOT NULL,
    email CHARACTER VARYING(100) NOT NULL UNIQUE,
    senha CHARACTER VARYING(255) NOT NULL,
    tipo_usuario CHARACTER VARYING(20) NOT NULL
);

-- Inserir alunos de exemplo
INSERT INTO alunos (aluno_id, nome, endereco, cidade, estado, cep, pais, telefone) VALUES
('A001', 'João Silva', 'Rua das Flores, 123', 'São Paulo', 'SP', '12345-678', 'Brasil', '11987654321'),
('A002', 'Maria Oliveira', 'Av. Central, 456', 'Rio de Janeiro', 'RJ', '23456-789', 'Brasil', '21987654322'),
('A003', 'Carlos Santos', 'Praça da Liberdade, 789', 'Belo Horizonte', 'MG', '34567-890', 'Brasil', '31987654323'),
('A004', 'Ana Costa', 'Rua do Sol, 101', 'Curitiba', 'PR', '45678-901', 'Brasil', '41987654324'),
('A005', 'Pedro Lima', 'Av. Paulista, 202', 'São Paulo', 'SP', '56789-012', 'Brasil', '11987654325');

-- Inserir professores de exemplo
INSERT INTO professores (professor_id, nome, departamento, email, telefone) VALUES
('P001', 'Carlos Almeida', 'Matemática', 'carlos.almeida@escola.com', '11987654321'),
('P002', 'Ana Souza', 'História', 'ana.souza@escola.com', '21987654322'),
('P003', 'João Pereira', 'Física', 'joao.pereira@escola.com', '31987654323');

-- Inserir pagamentos de exemplo
INSERT INTO pagamentos (aluno_id, valor, data_pagamento, metodo_pagamento) VALUES
('A001', 500.00, '2025-03-01', 'Cartão de Crédito'),
('A002', 300.00, '2025-03-05', 'Boleto Bancário'),
('A003', 450.00, '2025-03-10', 'Pix');

-- Inserir presenças de exemplo
INSERT INTO presencas (aluno_id, data, status) VALUES
('A001', '2025-03-01', 'Presente'),
('A002', '2025-03-01', 'Ausente'),
('A003', '2025-03-01', 'Presente');

-- Inserir atividades de exemplo
INSERT INTO atividades (titulo, descricao, data_entrega) VALUES
('Atividade 1', 'Descrição da atividade 1', '2025-03-15'),
('Atividade 2', 'Descrição da atividade 2', '2025-03-20');

-- Inserir atividades de alunos de exemplo
INSERT INTO atividades_alunos (atividade_id, aluno_id, status, nota) VALUES
(1, 'A001', 'Entregue', 9.5),
(1, 'A002', 'Pendente', NULL),
(2, 'A003', 'Entregue', 8.0);

-- Inserir usuários de exemplo
INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES
('Admin', 'admin@escola.com', 'admin123', 'Administrador'),
('Professor', 'professor@escola.com', 'prof123', 'Professor'),
('Aluno', 'aluno@escola.com', 'aluno123', 'Aluno');