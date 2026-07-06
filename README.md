# Sistema de Gerenciamento de Estoque

Sistema desenvolvido em Python para facilitar o controle de produtos, movimentações, estoque mínimo e geração de relatórios gerenciais. O projeto foi criado para organizar o gerenciamento de itens de forma prática, eficiente e intuitiva, com armazenamento local em SQLite.

---

## Demo

<div align="center">
  <img src="docs/2026-07-06-17_56_23 (online-video-cutter.com).gif" alt="Demonstração do Sistema de Gerenciamento de Estoque" width="100%" />
</div>

---

## Objetivo do Projeto

O Sistema de Gerenciamento de Estoque tem como objetivo ajudar negócios, estudantes ou equipes a controlar seus produtos com mais organização, reduzindo erros no registro de entradas e saídas e facilitando a análise do saldo disponível.

A aplicação foi criada para solucionar problemas como:

- perda de controle do estoque;
- dificuldade em acompanhar movimentações;
- falta de organização para tomadas de decisão gerenciais.

---

## Principais Funcionalidades

### Cadastro de Produtos
Registro completo de produtos com nome, categoria, fornecedor, preço, peso, quantidade, estoque mínimo, localização e identificação.

### Controle de Movimentações
Registro de entradas e saídas de produtos com histórico das operações realizadas.

### Consulta em Tempo Real
Visualização do estoque atual e do saldo disponível para cada item.

### Alertas de Estoque Baixo
Identificação automática de produtos com quantidade abaixo do mínimo definido.

### Relatórios Gerenciais
Geração de relatórios com informações importantes para análise do estoque e das operações.

---

## Tecnologias Utilizadas

### Back-end
- Python 3
- Django

### Banco de Dados
- SQLite

### Bibliotecas
- sqlite3
- pandas
- pathlib
- datetime
- math
- shutil

---

## Pré-requisitos para Executar o Projeto

- Python 3.8 ou superior
- pip
- SQLite (já incluso na instalação padrão do Python)

---

## Requisitos do Sistema

- interface simples e amigável no terminal;
- armazenamento local dos dados;
- organização eficiente do estoque;
- geração de relatórios para apoio à gestão.

---

## Estrutura do Projeto

```text
Sistema-de-gerenciador-de-estoque/
├── Cadastro.py
├── estoque_dados.py
├── estoque.db
├── manage.py
└── menu.py
```
