import datetime
import sqlite3
from pathlib import Path


# Caminho da pasta do projeto e do arquivo do banco.

BASE_DIR = Path(__file__).resolve().parent

CAMINHO_BANCO = BASE_DIR / "estoque.db"


def conectar_banco():
    
    # Abre uma conexao com o banco SQLite.
    
    return sqlite3.connect(CAMINHO_BANCO)


def preparar_banco():
    
    # Cria o banco e as tabelas, caso ainda nao existam.
    
    conexao = conectar_banco()
    
    cursor = conexao.cursor()
    

    # Tabela principal, onde ficam os produtos cadastrados.
    
    cursor.execute("""
                   
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identificacao TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL DEFAULT 'Sem categoria',
            fornecedor TEXT,
            preco REAL NOT NULL DEFAULT 0,
            peso REAL NOT NULL DEFAULT 0,
            quantidade INTEGER NOT NULL DEFAULT 0,
            estoque_minimo INTEGER NOT NULL DEFAULT 0,
            localizacao TEXT,
            tipo_enderecamento TEXT DEFAULT 'fixo',
            zona_armazenagem TEXT,
            sistema_identificacao TEXT DEFAULT 'manual',
            espe_tecnica TEXT,
            data_inicio TEXT NOT NULL,
            data_cadastro TEXT NOT NULL
        )
    """)

    # Tabela que guarda o historico de entradas e saidas.
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            produto_identificacao TEXT NOT NULL,
            tipo TEXT NOT NULL,
            motivo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL DEFAULT 0,
            valor_total REAL NOT NULL DEFAULT 0,
            saldo_apos_movimentacao INTEGER NOT NULL,
            observacao TEXT,
            data_movimentacao TEXT NOT NULL,
            FOREIGN KEY (produto_identificacao) REFERENCES produtos (identificacao)
        )
    """
    )

    conexao.commit()
    
    conexao.close()


def data_atual():
    
    # Retorna a data e hora no formato usado no sistema.
    
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def converter_data(data):
    
    # Aceita data vazia, objeto date ou texto em dois formatos.
    
    if not data:
        
        return datetime.date.today().strftime("%d/%m/%Y")
    
    if isinstance(data, datetime.date):
        
        return data.strftime("%d/%m/%Y")

    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        
        try:
            
            return datetime.datetime.strptime(str(data), formato).strftime("%d/%m/%Y")
        
        except ValueError:
            
            pass

    raise ValueError(f"Formato de data invalido: {data}")


def gerar_identificacao():
    
    # Gera um codigo unico para o produto.
    
    return f"PROD-{datetime.datetime.now():%Y%m%d%H%M%S%f}"


def produto_para_dict(produto):
    
    # Transforma a linha do banco em dicionario para facilitar o uso.
    
    return {
        
        "id": produto["id"],
        
        "identificacao": produto["identificacao"],
        
        "nome": produto["nome"],
        
        "categoria": produto["categoria"],
        
        "fornecedor": produto["fornecedor"],
        
        "preco": float(produto["preco"]),
        
        "peso": float(produto["peso"]),
        
        "quantidade": int(produto["quantidade"]),
        
        "estoque_minimo": int(produto["estoque_minimo"]),
        
        "localizacao": produto["localizacao"] or "",
        
        "tipo_enderecamento": produto["tipo_enderecamento"] or "fixo",
        
        "zona_armazenagem": produto["zona_armazenagem"] or "",
        
        "sistema_identificacao": produto["sistema_identificacao"] or "manual",
        
        "espe_tecnica": produto["espe_tecnica"] or "",
        
        "data_inicio": produto["data_inicio"],
        
        "data_cadastro": produto["data_cadastro"],
        
    }


def procurar_produto(conexao, nome_ou_id):
    
    # Procura pelo nome ou pela identificacao do produto.
    
    return conexao.execute(
        
        "SELECT * FROM produtos WHERE lower(nome) = lower(?) OR lower(identificacao) = lower(?) LIMIT 1",
        
        (nome_ou_id, nome_ou_id),
        
    ).fetchone()


def buscar_produto(nome_ou_id):
    
    # Busca um produto e devolve os dados dele em formato de dicionario.
    
    preparar_banco()
    
    conexao = conectar_banco()
    
    conexao.row_factory = sqlite3.Row
    
    produto = procurar_produto(conexao, nome_ou_id)
    
    conexao.close()

    if produto is None:
        
        raise ValueError(f"Produto '{nome_ou_id}' nao encontrado.")

    return produto_para_dict(produto)


def salvar_produto(dados):
    
    # Salva um produto novo ou atualiza um produto ja existente.
    
    preparar_banco()

    identificacao = dados.get("identificacao") or gerar_identificacao()
    
    valores = {
        
        "identificacao": identificacao,
        
        "nome": dados.get("nome"),
        
        "categoria": dados.get("categoria") or "Sem categoria",
        
        "fornecedor": dados.get("fornecedor") or None,
        
        "preco": float(dados.get("preco") or 0),
        
        "peso": float(dados.get("peso") or 0),
        
        "quantidade": int(dados.get("quantidade") or 0),
        
        "estoque_minimo": int(dados.get("estoque_minimo") or 0),
        
        "localizacao": dados.get("localizacao") or "",
        
        "tipo_enderecamento": dados.get("tipo_enderecamento") or "fixo",
        
        "zona_armazenagem": dados.get("zona_armazenagem") or "",
        
        "sistema_identificacao": dados.get("sistema_identificacao") or "manual",
        
        "espe_tecnica": dados.get("espe_tecnica") or "",
        
        "data_inicio": converter_data(dados.get("data_inicio")),
        
        "data_cadastro": data_atual(),
        
    }

    conexao = conectar_banco()
    
    conexao.row_factory = sqlite3.Row
    
    produto_antigo = conexao.execute(
        
        "SELECT data_cadastro FROM produtos WHERE identificacao = ?",
        
        (identificacao,),
        
    ).fetchone()

    atualizado = produto_antigo is not None
    
    if atualizado:
        
        # Se a identificacao ja existe, apenas atualiza o cadastro.
        
        valores["data_cadastro"] = produto_antigo["data_cadastro"]
        
        conexao.execute("""
            UPDATE produtos SET
                nome = :nome,
                categoria = :categoria,
                fornecedor = :fornecedor,
                preco = :preco,
                peso = :peso,
                quantidade = :quantidade,
                estoque_minimo = :estoque_minimo,
                localizacao = :localizacao,
                tipo_enderecamento = :tipo_enderecamento,
                zona_armazenagem = :zona_armazenagem,
                sistema_identificacao = :sistema_identificacao,
                espe_tecnica = :espe_tecnica,
                data_inicio = :data_inicio
            WHERE identificacao = :identificacao
        """, valores)
        
    else:
        
        # Se nao existe, cria um novo produto.
        
        conexao.execute("""
            INSERT INTO produtos (
                identificacao, nome, categoria, fornecedor, preco, peso,
                quantidade, estoque_minimo, localizacao, tipo_enderecamento,
                zona_armazenagem, sistema_identificacao, espe_tecnica,
                data_inicio, data_cadastro
            )
            VALUES (
                :identificacao, :nome, :categoria, :fornecedor, :preco, :peso,
                :quantidade, :estoque_minimo, :localizacao, :tipo_enderecamento,
                :zona_armazenagem, :sistema_identificacao, :espe_tecnica,
                :data_inicio, :data_cadastro
            )
            
        """, valores)

        if valores["quantidade"] > 0:
            
            # Quando cadastra com quantidade inicial, registra uma entrada.
            
            registrar_movimentacao(conexao, identificacao, "entrada", "cadastro",
                                   valores["quantidade"], valores["preco"],
                                   valores["quantidade"], "Cadastro inicial")

    conexao.commit()
    
    produto = conexao.execute(
        "SELECT * FROM produtos WHERE identificacao = ?",
        (identificacao,),
    ).fetchone()
    
    conexao.close()

    return produto_para_dict(produto), atualizado


def registrar_movimentacao(conexao, identificacao, tipo, motivo, quantidade, preco, saldo, observacao=""):
    
    # Grava no banco cada entrada ou saida feita no estoque.
    
    valor_total = float(preco or 0) * int(quantidade)
    
    codigo = f"MOV-{datetime.datetime.now():%Y%m%d%H%M%S%f}"

    conexao.execute("""
        INSERT INTO movimentacoes (
            codigo, produto_identificacao, tipo, motivo, quantidade,
            preco_unitario, valor_total, saldo_apos_movimentacao,
            observacao, data_movimentacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        
        codigo, identificacao, tipo, motivo, int(quantidade), float(preco or 0),
        valor_total, int(saldo), observacao, data_atual()
        
    ))


def registrar_entrada(nome_ou_id, quantidade, motivo="compra", preco_unitario=None, observacao=""):
    
    # Aumenta a quantidade do produto e registra a movimentacao.
    
    preparar_banco()
    
    quantidade = int(quantidade)
    
    if quantidade <= 0:
        
        raise ValueError("A quantidade deve ser maior que zero.")

    conexao = conectar_banco()
    
    conexao.row_factory = sqlite3.Row
    
    produto = procurar_produto(conexao, nome_ou_id)

    if produto is None:
        
        conexao.close()
        
        raise ValueError(f"Produto '{nome_ou_id}' nao encontrado.")

    saldo = int(produto["quantidade"]) + quantidade
    
    preco = produto["preco"] if preco_unitario is None else preco_unitario
    
    conexao.execute("UPDATE produtos SET quantidade = ? WHERE identificacao = ?", (saldo, produto["identificacao"]))
    
    registrar_movimentacao(conexao, produto["identificacao"], "entrada", motivo, quantidade, preco, saldo, observacao)
    
    conexao.commit()
    
    conexao.close()
    
    return buscar_produto(nome_ou_id)


def registrar_saida(nome_ou_id, quantidade, motivo="venda", observacao=""):
    
    # Diminui a quantidade do produto e registra a movimentacao.
    preparar_banco()
    
    quantidade = int(quantidade)
    
    if quantidade <= 0:
        
        raise ValueError("A quantidade deve ser maior que zero.")

    conexao = conectar_banco()
    
    conexao.row_factory = sqlite3.Row
    
    produto = procurar_produto(conexao, nome_ou_id)

    if produto is None:
        
        conexao.close()
        
        raise ValueError(f"Produto '{nome_ou_id}' nao encontrado.")
    
    if quantidade > int(produto["quantidade"]):
        
        conexao.close()
        
        raise ValueError("Quantidade de saida maior que o saldo disponivel.")

    saldo = int(produto["quantidade"]) - quantidade
    
    conexao.execute("UPDATE produtos SET quantidade = ? WHERE identificacao = ?", (saldo, produto["identificacao"]))
    
    registrar_movimentacao(conexao, produto["identificacao"], "saida", motivo, quantidade, produto["preco"], saldo, observacao)
    
    conexao.commit()
    
    conexao.close()
    
    return buscar_produto(nome_ou_id)


def listar_movimentacoes():
    
    # Lista as entradas e saidas, mostrando as mais recentes primeiro.
    
    preparar_banco()
    
    conexao = conectar_banco()
    
    conexao.row_factory = sqlite3.Row
    
    movimentacoes = conexao.execute("""
                                    
        SELECT m.*, p.nome AS produto
        FROM movimentacoes m
        JOIN produtos p ON p.identificacao = m.produto_identificacao
        ORDER BY m.id DESC
        
    """).fetchall()
    
    conexao.close()
    
    return [dict(movimento) for movimento in movimentacoes]


def consultar_saldo_atual():
    
    # Busca todos os produtos do banco e monta o estoque atual.
    
    preparar_banco()
    
    conexao = conectar_banco()
    
    conexao.row_factory = sqlite3.Row
    
    produtos = conexao.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
    
    conexao.close()

    estoque = {}
    
    for produto in produtos:
        
        dados = produto_para_dict(produto)
        
        estoque[dados["identificacao"]] = dados
        
    return estoque


def carregar_estoque():
    
    # Funcao usada pelo cadastro para carregar os produtos.
    
    return consultar_saldo_atual()


def consultar_estoque_baixo(limite=None):
    
    # Mostra os produtos que estao com pouca quantidade.
    
    estoque = carregar_estoque()
    
    produtos_baixos = []

    for produto in estoque.values():
        
        if limite is None:
            
            minimo = produto["estoque_minimo"]
            
        else:
            
            minimo = int(limite)

        if produto["quantidade"] <= minimo:
            
            produtos_baixos.append(produto)

    return produtos_baixos


def gerar_relatorio(indicadores=None):
    
    # Gera um resumo simples do estoque.
    
    if indicadores is None:
        
        indicadores = {}

    estoque = carregar_estoque()
    
    movimentacoes = listar_movimentacoes()

    quantidade_total = 0
    
    valor_total = 0
    
    total_entradas = 0
    
    total_saidas = 0
    
    cmv = 0
    
    por_categoria = {}
    
    por_motivo = {}

    for produto in estoque.values():
        
        quantidade_total += produto["quantidade"]
        
        valor_produto = produto["preco"] * produto["quantidade"]
        
        valor_total += valor_produto
        
        categoria = produto["categoria"]

        if categoria not in por_categoria:
            
            por_categoria[categoria] = {"quantidade": 0, "valor": 0}

        por_categoria[categoria]["quantidade"] += produto["quantidade"]
        
        por_categoria[categoria]["valor"] += valor_produto

    for movimento in movimentacoes:
        
        if movimento["tipo"] == "entrada":
            
            total_entradas += movimento["quantidade"]
            
        if movimento["tipo"] == "saida":
            
            total_saidas += movimento["quantidade"]
            
            cmv += movimento["valor_total"]

        motivo = movimento["motivo"]

        if motivo not in por_motivo:
            
            por_motivo[motivo] = {"quantidade": 0, "valor": 0}

        por_motivo[motivo]["quantidade"] += movimento["quantidade"]
        
        por_motivo[motivo]["valor"] += movimento["valor_total"]

    return {
        
        "total_produtos": len(estoque),
        
        "quantidade_total": quantidade_total,
        
        "valor_total_estoque": valor_total,
        
        "por_categoria": por_categoria,
        
        "total_entradas": total_entradas,
        
        "total_saidas": total_saidas,
        
        "cmv": cmv,
        
        "por_motivo": por_motivo,
        
        "giro_estoque": cmv / valor_total if valor_total else 0,
        
        "produtos_estoque_baixo": consultar_estoque_baixo(),
        
        "ultimas_movimentacoes": movimentacoes[:10],
        
        
    }


def gerar_pedidos_reposicao():
    
    # Ainda nao faz pedido automatico, so deixa a funcao pronta.
    
    return {"criados": [], "existentes": []}


def listar_pedidos_reposicao():
    
    # Como nao tem pedidos salvos, retorna lista vazia.
    
    return []


def processar_entrada(nome_ou_identificacao, quantidade, motivo="compra", preco_unitario=None, observacao=""):
    
    # Outro nome para registrar entrada.
    
    return registrar_entrada(nome_ou_identificacao, quantidade, motivo, preco_unitario, observacao)


def processar_saida(nome_ou_identificacao, quantidade, motivo="venda", observacao=""):
    
    # Outro nome para registrar saida.
    
    return registrar_saida(nome_ou_identificacao, quantidade, motivo, observacao)


gerar_relatorio_gerencial = gerar_relatorio

gerar_pedidos_reposicao_automaticos = gerar_pedidos_reposicao









