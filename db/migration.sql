CREATE DATABASE IF NOT EXISTS ecommerce;

USE ecommerce;

CREATE TABLE IF NOT EXISTS produto(
  id INT PRIMARY KEY,
  quantidade_estoque INT,
  descricao VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS vendedor(
  id INT PRIMARY KEY,
  nome VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS cliente(
  id INT PRIMARY KEY,
  nome VARCHAR(255),
  pais VARCHAR(255),
  regiao VARCHAR(255),
  cidade VARCHAR(255),
  endereco VARCHAR(255),
  email VARCHAR(255),
);

CREATE TABLE IF NOT EXISTS vendas(
  FOREIGN KEY (id_cliente) REFERENCES cliente(id),
  FOREIGN KEY (id_produto) REFERENCES produto(id),
  FOREIGN KEY (id_vendedor) REFERENCES vendedor(id),
  valor DECIMAL,
  data_venda DATE
);