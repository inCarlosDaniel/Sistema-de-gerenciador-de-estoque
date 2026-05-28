import datetime
import math
import shutil
 
import pandas as pd
 
from estoque_dados import (
    
    carregar_estoque,
    
    salvar_produto,
    
)
 
 
# Tamanhos maximos para alguns campos digitados pelo usuario.

TAMANHOS_MAXIMOS = {
    
    "nome": 100,
    "categoria": 100,
    "localizacao": 100,
    "zona_armazenagem": 100,
    "identificacao": 50,
    
}
 
# Nomes das colunas usadas na tabela de exibicao.

COLUNAS_TABELA = [
    
    "Nome",
    "Categoria",
    "Fornecedor",
    "Preco",
    "Peso",
    "Quantidade",
    "Estoque minimo",
    "Localizacao",
    "Identificacao",
    "Data de inicio",
    "Data de cadastro",
    
]

# Nome curto e largura maxima de cada coluna no terminal.
COLUNAS_EXIBICAO = {
    
    "Nome": ("Nome", 10),
    "Categoria": ("Cat", 6),
    "Fornecedor": ("Fornec", 8),
    "Preco": ("Preco", 8),
    "Peso": ("Peso", 5),
    "Quantidade": ("Qtd", 3),
    "Estoque minimo": ("Min", 3),
    "Localizacao": ("Local", 8),
    "Identificacao": ("ID", 14),
    "Data de inicio": ("Inicio", 10),
    "Data de cadastro": ("Cadastro", 10),
    
}
 
matriz = []
 
 

# VALIDAÇÕES

 
def validar_tamanho(valor, campo, tamanho_maximo):
    
    # Verifica se o texto nao passou do tamanho permitido.
    
    if valor and len(str(valor)) > tamanho_maximo:
        
        raise ValueError(f"{campo} deve ter no máximo {tamanho_maximo} caracteres.")
    

def validar_nome_produto(nome):
    
    # Evita salvar caminho ou comando no lugar do nome do produto.
    
    texto = nome.lower()
    
    if texto.startswith("/") or "conda activate" in texto:
        
        raise ValueError("O nome do produto parece ser um caminho ou comando.")
    
 
 
def ler_numero_positivo(mensagem):
    
    # Le um numero decimal e nao deixa aceitar valor negativo.
    
    try:
        
        valor = float(input(mensagem).replace(",", "."))
        
    except ValueError as erro:
        
        raise ValueError("Digite um número válido.") from erro
    
 
    if not math.isfinite(valor) or valor < 0:
        
        raise ValueError("Digite um número válido e positivo.")
    
 
    return valor
 
 
def ler_inteiro_nao_negativo(mensagem):
    
    # Le um numero inteiro e nao deixa aceitar valor negativo.
    
    try:
        
        valor = int(input(mensagem))
        
    except ValueError as erro:
        
        raise ValueError("Digite um número inteiro válido.") from erro
    
 
    if valor < 0:
        
        raise ValueError("Digite um número inteiro maior ou igual a zero.")
 
    return valor
 
 

# TABELA / MATRIZ
 
def produto_para_linha(produto, identificacao=None):
    
    # Converte o dicionario do produto em uma linha para a tabela.

    return [
        
        produto["nome"],
        produto.get("categoria", "Sem categoria"),
        formatar_fornecedor(produto.get("fornecedor")),
        produto["preco"],
        produto["peso"],
        produto["quantidade"],
        produto.get("estoque_minimo", 0),
        produto.get("localizacao", ""),
        identificacao or produto.get("identificacao", ""),
        produto.get("data_inicio", ""),
        produto.get("data_cadastro", ""),
        
    ]


def formatar_fornecedor(fornecedor):
    
    # Se o fornecedor vier como dicionario, pega so o nome.
    
    if isinstance(fornecedor, dict):
        
        return fornecedor.get("nome", "")
    
    return fornecedor or ""
 
 
def atualizar_matriz(estoque):
    
    # Atualiza a matriz usada para montar a tabela.
    
    matriz.clear()
    
    for identificacao, produto in estoque.items():
        
        matriz.append(produto_para_linha(produto, identificacao))
        
    return matriz
 
 
def criar_tabela_estoque(estoque=None):
    
    # Cria um DataFrame do pandas para facilitar a exibicao.
    
    if estoque is None:
        
        estoque = carregar_estoque()
 
    dados = atualizar_matriz(estoque)
    
    return pd.DataFrame(dados, columns=COLUNAS_TABELA)


def formatar_valor_tabela(coluna, valor):
    
    # Ajusta alguns valores antes de mostrar na tela.
    
    if coluna == "Preco":
        
        return f"R$ {float(valor):.2f}"
    
    if coluna == "Peso":
        
        return f"{float(valor):.2f}"
    
    if coluna == "Data de cadastro":
        
        return str(valor)[:10]
    
    return str(valor)


def limitar_texto(texto, largura):
    
    # Corta textos grandes para a tabela caber melhor no terminal.
    
    texto = str(texto)
    
    if len(texto) <= largura:
        
        return texto
    
    if largura <= 1:
        
        return texto[:largura]
    
    return texto[:largura - 1] + "~"


def imprimir_tabela_com_linhas(tabela):
    
    # Imprime a tabela manualmente com bordas.
    
    colunas = [
        
        coluna
        
        for coluna in tabela.columns
        
        if coluna in COLUNAS_EXIBICAO
        
    ]
    cabecalhos = [COLUNAS_EXIBICAO[coluna][0] for coluna in colunas]
    
    larguras_maximas = [COLUNAS_EXIBICAO[coluna][1] for coluna in colunas]
    
    linhas = [
        
        [
            
            limitar_texto(formatar_valor_tabela(coluna, linha[coluna]), largura)
            
            for coluna, largura in zip(colunas, larguras_maximas)
            
        ]
        
        for _, linha in tabela.iterrows()
        
    ]

    larguras = [
        
        max(len(cabecalho), max([len(linha[indice]) for linha in linhas], default=0))
        
        for indice, cabecalho in enumerate(cabecalhos)
        
    ]

    largura_total = sum(larguras) + (len(larguras) * 3) + 1
    
    largura_terminal = shutil.get_terminal_size((120, 20)).columns
    
    if largura_total > largura_terminal:
        
        print("(Tabela compactada para caber no terminal.)")

    def separador():
        
        return "+" + "+".join("-" * (largura + 2) for largura in larguras) + "+"

    def montar_linha(valores):
        
        celulas = [
            
            f" {valor:<{largura}} "
            
            for valor, largura in zip(valores, larguras)
            
        ]
        
        return "|" + "|".join(celulas) + "|"

    print(separador())
    
    print(montar_linha(cabecalhos))
    
    print(separador())
    
    for linha in linhas:
        
        print(montar_linha(linha))
        
    print(separador())
 
 

# CADASTRO

def cadastrar_produto(estoque, produto, mostrar_mensagem=True):
    
    # Salva o produto no banco e atualiza o estoque em memoria.
    
    produto_salvo, atualizado = salvar_produto(produto)
    
    nome = produto_salvo["nome"]
 
    estoque.clear()
    
    estoque.update(carregar_estoque())
    
    atualizar_matriz(estoque)
 
    if mostrar_mensagem:
        
        if atualizado:
            
            print(f"Produto '{nome}' atualizado com sucesso.")
            
        else:
            
            print(f"Produto '{nome}' salvo com sucesso.")
            
 
    return produto_salvo
 
 
def solicitar_dados_produto():
    # Pergunta ao usuario os dados do produto pelo terminal.
    
    print("\nCadastro de Produtos")
 
    nome = input("Nome do produto: ").strip()
    
    if not nome:
        
        raise ValueError("O nome do produto é obrigatório.")
    
    validar_tamanho(nome, "Nome", TAMANHOS_MAXIMOS["nome"])
    
    validar_nome_produto(nome)
 
    categoria = input("Categoria: ").strip() or "Sem categoria"
    
    validar_tamanho(categoria, "Categoria", TAMANHOS_MAXIMOS["categoria"])
 
    # Fornecedor fica salvo como texto simples.
    fornecedor = input("Fornecedor: ").strip()
 
    preco = ler_numero_positivo("Preço: ")
    
    peso = ler_numero_positivo("Peso: ")
    
    quantidade = ler_inteiro_nao_negativo("Quantidade em estoque: ")
 
    estoque_minimo_raw = input("Estoque mínimo (enter para 0): ").strip()
    
    if estoque_minimo_raw:
        
        try:
            
            estoque_minimo = int(estoque_minimo_raw)
            
        except ValueError as erro:
            
            raise ValueError("O estoque mínimo deve ser um número inteiro.") from erro
        
        if estoque_minimo < 0:
            
            raise ValueError("O estoque mínimo deve ser maior ou igual a zero.")
    else:
        
        estoque_minimo = 0
 
    localizacao = input("Localização (opcional): ").strip()
    
    validar_tamanho(localizacao, "Localização", TAMANHOS_MAXIMOS["localizacao"])
 
    identificacao = input("Identificação (enter para gerar automático): ").strip()
    
    if identificacao:
        
        validar_tamanho(identificacao, "Identificação", TAMANHOS_MAXIMOS["identificacao"])
 
    data_inicio = input("Data de início dd/mm/aaaa (enter para hoje): ").strip()
    
    if not data_inicio:
        
        data_inicio = datetime.date.today().strftime("%d/%m/%Y")
 
    return {
        
        "nome": nome,
        "categoria": categoria,
        "fornecedor": fornecedor or None,
        "preco": preco,
        "peso": peso,
        "quantidade": quantidade,
        "estoque_minimo": estoque_minimo,
        "localizacao": localizacao,
        "identificacao": identificacao or None,   # None = gera automático no estoque_dados
        "data_inicio": data_inicio,
        
    }
 
 

# EXIBIÇÃO

 
def exibir_estoque(estoque=None):
    
    # Mostra todos os produtos cadastrados.
    
    print("\nEstoque atual:")
 
    if estoque is None:
        
        estoque = carregar_estoque()
 
    if not estoque:
        
        print("Nenhum produto cadastrado.")
        
        return
 
    tabela = criar_tabela_estoque(estoque)
    
    imprimir_tabela_com_linhas(tabela)
 
# EXECUÇÃO

def executar_cadastro():
    
    # Loop principal: cadastra produtos ate o usuario escolher parar.
   
    estoque = carregar_estoque()
 
    while True:
        
        try:
            
            produto = solicitar_dados_produto()
            
            cadastrar_produto(estoque, produto)
            
            exibir_estoque(estoque)
            
        except ValueError as erro:
            
            print(f"Erro: {erro}")
 
        continuar = input("\nCadastrar outro produto? [s/N]: ").strip().lower()
        
        if continuar not in ("s", "sim"):
            
            break
 
    return estoque
 
 
if __name__ == "__main__":
    
    # Roda o cadastro quando este arquivo e executado diretamente.
    
    executar_cadastro()
