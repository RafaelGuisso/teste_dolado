-- Esse codigo foi feito utilizando o MySQL

-- Criando o Banco de Dados e o Schema a serem utilizados
CREATE DATABASE IF NOT EXISTS teste_rafael;
USE teste_rafael;
CREATE SCHEMA IF NOT EXISTS rafael_schema;


-- Criei a tabela comissoes seguindo as instruções recomendadas na questão
CREATE TABLE IF NOT EXISTS comissoes (
  comprador VARCHAR(255) NOT NULL,
  vendedor VARCHAR(255) NOT NULL,
  dataPgto DATE NOT NULL,
  valor FLOAT NOT NULL
);

-- Vou inserir os dados da questão dentro de "comissoes"
INSERT IGNORE INTO comissoes (comprador, vendedor, dataPgto, valor) VALUES
('Leonardo', 'Bruno', '2000-01-01', 200.00),
('Leonardo', 'Matheus', '2003-09-27', 1024.00),
('Leonardo', 'Lucas', '2006-06-26', 512.00),
('Marcos', 'Lucas', '2020-12-17', 100.00),
('Marcos', 'Lucas', '2002-03-22', 10.00),
('Cinthia', 'Lucas', '2021-03-20', 500.00),
('Mateus', 'Bruno', '2007-06-02', 400.00),
('Mateus', 'Bruno', '2006-06-26', 400.00),
('Mateus', 'Bruno', '2015-06-26', 200.00);

SELECT * from comissoes;

-- Caso a tabela esteja duplicada, utilize o drop table abaixo e rode o código novamente
-- drop table comissoes




