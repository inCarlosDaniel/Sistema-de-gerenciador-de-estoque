# Sistema de gerenciador de estoque

Programa em Python para gerenciamento de estoque, com cadastro de produtos, registro de movimentações, consulta do saldo atual, alertas de estoque baixo e geração de relatórios gerenciais.

## Funcionalidades

- Cadastro de produtos com nome, categoria, fornecedor, preço, peso, quantidade, estoque mínimo, localização e identificação.
- Geração automática de identificação do produto quando o usuário não informa uma.
- Armazenamento dos dados em banco SQLite.
- Registro de entradas e saídas de produtos.
- Histórico de movimentações do estoque.
- Consulta do estoque atual em tempo real.
- Alerta de produtos com estoque baixo.
- Relatórios gerenciais com:
  - total de produtos cadastrados;
  - quantidade total em estoque;
  - valor total do estoque;
  - produtos por categoria;
  - total de entradas;
  - total de saídas;
  - CMV;
  - giro de estoque;
  - últimas movimentações.

## Tecnologias utilizadas

- Python
- SQLite
- Pandas

## Bibliotecas utilizadas

- `datetime`: usada para trabalhar com datas e horários, como data de cadastro, data de início e códigos gerados com data.
- `math`: usada para validar números, garantindo que valores como preço e peso sejam válidos.
- `shutil`: usada para identificar o tamanho do terminal e ajustar a exibição da tabela.
- `sqlite3`: usada para criar e acessar o banco de dados SQLite.
- `pathlib`: usada para trabalhar com caminhos de arquivos e localizar o banco `estoque.db`.
- `pandas`: usada para criar e exibir a tabela de estoque em formato de DataFrame.

## Estrutura do projeto

```text
Sistema-de-gerenciador-de-estoque/
├── Cadastro.py
├── estoque_dados.py
├── estoque.db
└── menu.py
