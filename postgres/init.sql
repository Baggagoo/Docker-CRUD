-- Script to initialize the "escola" database

-- Create the database
CREATE DATABASE escola;

-- Connect to the "escola" database
\c escola;

-- Create the "alunos" table with the specified fields
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

-- Insert at least 10 sample students
INSERT INTO alunos (aluno_id, nome, endereco, cidade, estado, cep, pais, telefone) VALUES
('A001', 'João Silva', 'Rua das Flores, 123', 'São Paulo', 'SP', '12345-678', 'Brasil', '11987654321'),
('A002', 'Maria Oliveira', 'Av. Central, 456', 'Rio de Janeiro', 'RJ', '23456-789', 'Brasil', '21987654322'),
('A003', 'Carlos Santos', 'Praça da Liberdade, 789', 'Belo Horizonte', 'MG', '34567-890', 'Brasil', '31987654323'),
('A004', 'Ana Costa', 'Rua do Sol, 101', 'Curitiba', 'PR', '45678-901', 'Brasil', '41987654324'),
('A005', 'Pedro Lima', 'Av. Paulista, 202', 'São Paulo', 'SP', '56789-012', 'Brasil', '11987654325'),
('A006', 'Fernanda Souza', 'Rua das Palmeiras, 303', 'Salvador', 'BA', '67890-123', 'Brasil', '71987654326'),
('A007', 'Lucas Almeida', 'Av. Atlântica, 404', 'Florianópolis', 'SC', '78901-234', 'Brasil', '48987654327'),
('A008', 'Juliana Rocha', 'Rua das Acácias, 505', 'Porto Alegre', 'RS', '89012-345', 'Brasil', '51987654328'),
('A009', 'Rafael Mendes', 'Av. Brasil, 606', 'Fortaleza', 'CE', '90123-456', 'Brasil', '85987654329'),
('A010', 'Beatriz Carvalho', 'Rua do Campo, 707', 'Recife', 'PE', '01234-567', 'Brasil', '81987654330');