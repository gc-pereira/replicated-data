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