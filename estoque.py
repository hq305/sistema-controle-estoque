import os
import time
import sqlite3

pasta_dados = 'dados'
banco = os.path.join(pasta_dados, 'estoque.db')
tempo_de_espera = 2


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def conexao():
    os.makedirs(pasta_dados, exist_ok=True)  # cria a pasta se ela não existir
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()
    return conn, cursor


def criar_tabela():
    conn, cursor = conexao()
    cursor.execute('CREATE TABLE IF NOT EXISTS produtos(nome TEXT, preco REAL, quantidade INTEGER)')
    conn.commit()
    conn.close()


def cadastro_produto():
    try:
        produto = input("digite o nome do produto: ").strip()# remove espaços em branco
        preco = float(input('digite o preço do produto: '))
        quantidade = int(input('digite a quantidade do produto: '))
    except ValueError:
        print('Digite um valor válido!')
        time.sleep(tempo_de_espera)
        return

    if not produto:
        print('O nome não pode ser vazio!')
        time.sleep(tempo_de_espera)
        return
    if preco <= 0:
        print('O preço deve ser maior que zero!')
        time.sleep(tempo_de_espera)
        return
    if quantidade < 0:
        print('A quantidade não pode ser negativa!')
        time.sleep(tempo_de_espera)
        return

    conn, cursor = conexao()
    cursor.execute("SELECT nome FROM produtos WHERE LOWER(nome) = LOWER(?)", (produto,))
    if cursor.fetchone():
        conn.close()
        limpar_tela()
        print('produto ja cadastrado!')
    else:
        cursor.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)",
                       (produto, preco, quantidade))
        conn.commit()
        conn.close()
        limpar_tela()
        print('produto cadastrado!')
    time.sleep(tempo_de_espera)


def listar_produtos():
    conn, cursor = conexao()
    cursor.execute("SELECT * FROM produtos")
    produtos_do_banco = cursor.fetchall()
    conn.close()

    limpar_tela()

    if not produtos_do_banco:
        print('Não tem produtos cadastrados')
    else:
        print('===== LISTA DE PRODUTOS =====\n')
        for produto, preco, quantidade in produtos_do_banco:
            print(f'Produto: {produto}')
            print(f'Preço: R${preco:.2f}')
            print(f'Quantidade: {quantidade}')
            print('-' * 25)

    input("\nPressione Enter para voltar ao menu...")


def buscar_produto():
    limpar_tela()
    busca = input("digite o nome do produto: ").strip()

    conn, cursor = conexao()
    cursor.execute("SELECT nome, preco, quantidade FROM produtos WHERE LOWER(nome) = LOWER(?)", (busca,))
    resultado = cursor.fetchone()
    conn.close()

    limpar_tela()
    if resultado:
        print('produto encontrado!')
        print(f'produto: {resultado[0]}')
        print(f'preco: R${resultado[1]:.2f}')
        print(f'quantidade: {resultado[2]}')
        print()

        input("\nPressione Enter para voltar ao menu...")

    else:
        print('produto nao encontrado!')
        time.sleep(tempo_de_espera)


def adicionar_estoque():
    limpar_tela()
    nome = input('Digite o nome do produto que voce deseja adicionar: ').strip()

    conn, cursor = conexao()
    cursor.execute("SELECT nome, quantidade FROM produtos WHERE LOWER(nome) = LOWER(?)", (nome,))
    resultado = cursor.fetchone()

    if not resultado:
        conn.close()
        limpar_tela()
        print("produto nao encontrado!")
        time.sleep(tempo_de_espera)
        return

    limpar_tela()
    print('Produto encontrado!')
    print(f'Produto: {resultado[0]}')
    print(f'Estoque atual: {resultado[1]}')
    print()

    try:
        estoque = int(input('digite a quantidade que deseja adicionar: '))
    except ValueError:
        conn.close()
        limpar_tela()
        print('Digite um valor válido!')
        time.sleep(tempo_de_espera)
        return

    if estoque <= 0:
        conn.close()
        limpar_tela()
        print('A quantidade deve ser maior que zero!')
        time.sleep(tempo_de_espera)
        return

    cursor.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE LOWER(nome) = LOWER(?)",
                   (estoque, nome))
    conn.commit()
    conn.close()

    limpar_tela()
    print('estoque atualizado!')
    print()
    print(f"produto: {resultado[0]}")
    print(f"estoque: {resultado[1] + estoque}")
    print()
    time.sleep(tempo_de_espera)


def remover_estoque():
    limpar_tela()
    nome = input('Digite o nome do produto que voce deseja remover: ').strip()

    conn, cursor = conexao()
    cursor.execute("SELECT nome, quantidade FROM produtos WHERE LOWER(nome) = LOWER(?)", (nome,))
    resultado = cursor.fetchone()

    if not resultado:
        conn.close()
        limpar_tela()
        print("produto nao encontrado!")
        time.sleep(tempo_de_espera)
        return

    limpar_tela()
    print('Produto encontrado!')
    print(f'Produto: {resultado[0]}')
    print(f'Estoque atual: {resultado[1]}')
    print()

    try:
        estoque = int(input('digite a quantidade que deseja remover: '))
    except ValueError:
        conn.close()
        limpar_tela()
        print('Digite um valor válido!')
        time.sleep(tempo_de_espera)
        return

    if estoque <= 0:
        conn.close()
        limpar_tela()
        print('A quantidade deve ser maior que zero!')
        time.sleep(tempo_de_espera)
        return

    if resultado[1] < estoque:
        conn.close()
        limpar_tela()
        print('Estoque insuficiente!')
        time.sleep(tempo_de_espera)
        return

    cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE LOWER(nome) = LOWER(?)",
                   (estoque, nome))
    conn.commit()
    conn.close()

    limpar_tela()
    print('estoque atualizado!')
    print()
    print(f"produto: {resultado[0]}")
    print(f"estoque: {resultado[1] - estoque}")
    print()
    time.sleep(tempo_de_espera)


def valor_total():
    conn, cursor = conexao()
    cursor.execute("SELECT SUM(preco * quantidade) FROM produtos")
    resultado = cursor.fetchone()
    conn.close()

    estoque_total = resultado[0] if resultado[0] is not None else 0
    limpar_tela()
    print(f"Valor total do estoque: R${estoque_total:.2f}")

    input("\nPressione Enter para voltar ao menu...")


def main():
    criar_tabela()
    while True:
        print('===== SISTEMA DE ESTOQUE =====')
        print('1 - Cadastrar produto')
        print('2 - Listar produtos')
        print('3 - Buscar produto')
        print('4 - Adicionar estoque')
        print('5 - Remover estoque')
        print('6 - Mostrar valor total do estoque')
        print('7 - Sair')

        opcao = input('Escolha uma opcao: ').strip()
        limpar_tela()

        if opcao == '1':
            cadastro_produto()
        elif opcao == '2':
            listar_produtos()
        elif opcao == '3':
            buscar_produto()
        elif opcao == '4':
            adicionar_estoque()
        elif opcao == '5':
            remover_estoque()
        elif opcao == '6':
            valor_total()
        elif opcao == '7':
            print('saindo...')
            time.sleep(tempo_de_espera)
            break
        else:
            print('Opção inválida!')
            time.sleep(tempo_de_espera)

        limpar_tela()


if __name__ == '__main__':
    main()