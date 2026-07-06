# Importa as funcoes do arquivo Cadastro.py usadas no menu.

from Cadastro import cadastrar_produto, exibir_estoque, solicitar_dados_produto

# Importa as funcoes do arquivo estoque_dados.py para acessar o banco e movimentacoes.

from estoque_dados import (
    
    carregar_estoque,
    consultar_estoque_baixo,
    gerar_relatorio,
    listar_movimentacoes,
    registrar_entrada,
    registrar_saida,
    
)


def pausar():
    
    # Pausa a tela para o usuario conseguir ler o resultado antes de voltar ao menu.
    
    input("\nPressione Enter para continuar...")


def mostrar_titulo(texto):
    
    # Mostra um titulo padronizado para separar as telas do sistema.
    
    print("\n" + "=" * 50)
    
    print(texto)
    
    print("=" * 50)


def cadastrar():
    
    # Chama a tela de cadastro de produto e salva os dados no banco.
    
    mostrar_titulo("Cadastrar produto")
    
    estoque = carregar_estoque()
    
    produto = solicitar_dados_produto()
    
    cadastrar_produto(estoque, produto)


def consultar_estoque():
    
    # Carrega o estoque atualizado do banco e mostra em formato de tabela.
    
    mostrar_titulo("Estoque atual")
    
    exibir_estoque(carregar_estoque())


def entrada_produto():
    
    # Registra uma entrada, aumentando a quantidade do produto no estoque.
    
    mostrar_titulo("Registrar entrada")
    
    produto = input("Nome ou identificacao do produto: ").strip()
    
    quantidade = int(input("Quantidade de entrada: "))
    
    motivo = input("Motivo (enter para compra): ").strip() or "compra"
    
    preco = input("Preco unitario (enter para usar preco cadastrado): ").strip()
    
    observacao = input("Observacao (opcional): ").strip()

    preco_unitario = float(preco.replace(",", ".")) if preco else None
    
    produto_atualizado = registrar_entrada(
        
        produto,
        quantidade,
        motivo=motivo,
        preco_unitario=preco_unitario,
        observacao=observacao,
        
    )

    print(f"Entrada registrada. Saldo atual: {produto_atualizado['quantidade']}")


def saida_produto():
    
    # Registra uma saida, diminuindo a quantidade do produto no estoque.
    
    mostrar_titulo("Registrar saida")
    
    produto = input("Nome ou identificacao do produto: ").strip()
    
    quantidade = int(input("Quantidade de saida: "))
    
    motivo = input("Motivo (enter para venda): ").strip() or "venda"
    
    observacao = input("Observacao (opcional): ").strip()
    

    produto_atualizado = registrar_saida(
        produto,
        quantidade,
        motivo=motivo,
        observacao=observacao,
    )

    print(f"Saida registrada. Saldo atual: {produto_atualizado['quantidade']}")


def mostrar_movimentacoes():
    
    # Mostra o historico de entradas e saidas ja registradas.
    
    mostrar_titulo("Historico de movimentacoes")
    
    movimentacoes = listar_movimentacoes()
    

    if not movimentacoes:
        
        print("Nenhuma movimentacao registrada.")
        
        return

    for movimento in movimentacoes:
        
        print(
            
            f"{movimento['data_movimentacao']} | "
            
            f"{movimento['produto']} | "
            
            f"{movimento['tipo']} | "
            
            f"Qtd: {movimento['quantidade']} | "
            
            f"Motivo: {movimento['motivo']} | "
            
            f"Saldo: {movimento['saldo_apos_movimentacao']}"
            
        )


def mostrar_estoque_baixo():
    
    # Lista os produtos cuja quantidade esta menor ou igual ao estoque minimo.
    
    mostrar_titulo("Produtos com estoque baixo")
    
    produtos = consultar_estoque_baixo()

    if not produtos:
        
        print("Nenhum produto com estoque baixo.")
        
        return

    for produto in produtos:
        
        print(
            
            f"{produto['nome']} | "
            
            f"Qtd: {produto['quantidade']} | "
            
            f"Minimo: {produto['estoque_minimo']} | "
            
            f"ID: {produto['identificacao']}"
        )


def mostrar_relatorio():
    
    # Gera e mostra os principais indicadores gerenciais do estoque.
    
    mostrar_titulo("Relatorio gerencial")
    
    relatorio = gerar_relatorio()

    print(f"Total de produtos: {relatorio['total_produtos']}")
    
    print(f"Quantidade total em estoque: {relatorio['quantidade_total']}")
    
    print(f"Valor total do estoque: R$ {relatorio['valor_total_estoque']:.2f}")
    
    print(f"Total de entradas: {relatorio['total_entradas']}")
    
    print(f"Total de saidas: {relatorio['total_saidas']}")
    
    print(f"CMV: R$ {relatorio['cmv']:.2f}")
    
    print(f"Giro de estoque: {relatorio['giro_estoque']:.2f}")

    print("\nProdutos por categoria:")
    
    if relatorio["por_categoria"]:
        
        for categoria, dados in relatorio["por_categoria"].items():
            
            print(
                f"- {categoria}: "
                f"{dados['quantidade']} unidades | "
                f"R$ {dados['valor']:.2f}"
            )
            
    else:
        
        print("Nenhuma categoria encontrada.")

    print("\nUltimas movimentacoes:")
    
    if relatorio["ultimas_movimentacoes"]:
        
        for movimento in relatorio["ultimas_movimentacoes"]:
            
            print(
                
                f"- {movimento['produto']} | "
                
                f"{movimento['tipo']} | "
                
                f"Qtd: {movimento['quantidade']} | "
                
                f"{movimento['data_movimentacao']}"
                
            )
            
    else:
        
        print("Nenhuma movimentacao encontrada.")


def mostrar_menu():
    
    # Exibe as opcoes disponiveis para o usuario escolher.
    
    print("\nSistema de Gerenciador de Estoque")
    print("1 - Cadastrar produto")
    
    print("2 - Consultar estoque atual")
    
    print("3 - Registrar entrada")
    
    print("4 - Registrar saida")
    
    print("5 - Ver historico de movimentacoes")
    
    print("6 - Ver produtos com estoque baixo")
    
    print("7 - Gerar relatorio gerencial")
    
    print("0 - Sair")


def executar_menu():
    
    # Mantem o sistema rodando ate o usuario escolher a opcao 0.
    
    while True:
        
        mostrar_menu()
        
        opcao = input("Escolha uma opcao: ").strip()
        

        try:
            
            # Direciona o usuario para a funcao correta de acordo com a opcao escolhida.
            
            if opcao == "1":
                
                cadastrar()
                
            elif opcao == "2":
                
                consultar_estoque()
            elif opcao == "3":
                
                entrada_produto()
                
            elif opcao == "4":
                
                saida_produto()
                
            elif opcao == "5":
                
                mostrar_movimentacoes()
                
            elif opcao == "6":
                
                mostrar_estoque_baixo()
                
            elif opcao == "7":
                
                mostrar_relatorio()
                
            elif opcao == "0":
                
                print("Saindo do sistema...")
                
                break
            
            else:
                
                print("Opcao invalida.")
                
        except ValueError as erro:
            
            # Mostra erros de validacao sem fechar o sistema.
            print(f"Erro: {erro}")
            

        if opcao != "0":
            
            pausar()


if __name__ == "__main__":
    
    # Executa o menu somente quando este arquivo for iniciado diretamente.
    
    executar_menu()
