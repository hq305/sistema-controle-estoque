import os
import time
import sqlite3

def conexao():
    conn = sqlite3.connect('dados/estoque.db')
    cursor = conn.cursor()
    return conn, cursor

def criar_tabela():
    conn, cursor = conexao()
    cursor.execute('CREATE TABLE IF NOT EXISTS produtos(nome TEXT, preco REAL, quantidade INTEGER)'
                   )
    conn.commit()
    conn.close()



tempo_de_espera = 2
def cadastro_produto():
    try:
        produto = input("digite o nome do produto: ").strip()
        preco = float(input('digite o preço do produto: '))
        quantidade = int(input('digite a quantidado do produto: '))
        if preco < 0:
            print('preco negativo! ')
            return
        if quantidade < 0:
            print('quantidade negativa!')
            return 

    except ValueError:
        print('Digite um valor válido!')
        return None
    else:
        conn, cursor = conexao()
        cursor.execute("SELECT nome FROM produtos WHERE LOWER(nome) = LOWER(?)", (produto,))
        resultado = cursor.fetchone()
        if resultado:
            conn.close()
            os.system('cls')
            print('produto ja cadastrado! ')
            time.sleep(tempo_de_espera)
        else:
            cursor.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (produto, preco, quantidade))
            conn.commit()
            conn.close()
            os.system('cls')
            print('produto cadastrado! ')
            time.sleep(tempo_de_espera)
        

def listar_produtos():
    conn, cursor = conexao()
    cursor.execute("SELECT * FROM produtos")
    produtos_do_banco = cursor.fetchall()
    os.system('cls')
    if not produtos_do_banco:
        print('Nao tem produtos cadastrados')
    else:
        for l in produtos_do_banco:
            os.system('cls')
            produto, preco ,quantidade = l
            print(f'produto: {produto}')
            print(f'preco: R${preco:.2f}')
            print(f'quantidade: {quantidade}')
            print()
            time.sleep(tempo_de_espera)

def buscar_produto():
    conn,cursor = conexao()
    os.system('cls')
    busca = input("digite o nome do produto: ").strip()
    cursor.execute("SELECT nome, preco, quantidade FROM produtos WHERE LOWER(nome) = LOWER(?)",(busca,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        os.system('cls')
        print('produto encontrado!')
        print(f'produto: {resultado[0]}')
        print(f'preco: R${resultado[1]:.2f}')
        print(f'quantidade: {resultado[2]}')
        print()
        time.sleep(tempo_de_espera)
    else:
        os.system('cls')
        print('produto nao encontrado! ')
        time.sleep(tempo_de_espera)

def adicionar_estoque():
    conn, cursor = conexao()
    nome = input('Digite o nome do produto que voce deseja adicionar: ').strip()
    cursor.execute("SELECT nome, quantidade FROM produtos WHERE LOWER(nome) = LOWER(?)",(nome,))
    resultado = cursor.fetchone()
    if resultado:
            os.system('cls')
            print('Produto encontrado!')
            print(f'Produto: {resultado[0]}')
            print(f'Estoque atual: {resultado[1]}')
            print()
            time.sleep(tempo_de_espera)
            try:
                estoque = int(input('digite a quantidade que deseja adicionar: '))
                if estoque < 0:
                    os.system('cls')
                    print('Quantidade inválida!')
                    conn.close()
                    return
                cursor.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE LOWER(nome) = LOWER(?)",(estoque, nome))
                conn.commit()
                
            except ValueError:
                os.system('cls')
                print('Digite um valor valido! ')
                conn.close()
                return
            os.system('cls')
            print('estoque atualizado! ')
            print()
            print(f"produto: {resultado[0]}")
            print(f"estoque: {resultado[1] + estoque}")
            print()
            conn.close()
            return
    conn.close()
    os.system('cls')
    print("produto nao encontrado!")

def remover_estoque():
    conn, cursor = conexao()
    nome = input('Digite o nome do produto que voce deseja remover: ').strip()
    cursor.execute("SELECT nome, quantidade FROM produtos WHERE LOWER(nome) = LOWER(?)",(nome,))
    resultado = cursor.fetchone()
    if resultado:
        os.system('cls')
        print('Produto encontrado!')
        print(f'Produto: {resultado[0]}')
        print(f'Estoque atual: {resultado[1]}')
        print()
        time.sleep(tempo_de_espera)
        try:
                estoque = int(input('digite a quantidade que deseja remover: '))
        except ValueError:
                os.system('cls')
                print('Digite um valor válido!')
                conn.close()
                return
        if estoque < 0:
                os.system('cls')
                print('Quantidade inválida!')
                conn.close()
                return
        if resultado[1] < estoque:
                os.system('cls')
                print('Estoque insuficiente')
                conn.close()
                return
        cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE LOWER(nome) = LOWER(?)", (estoque, nome,))
        conn.commit()
                
        os.system('cls')
        print('estoque atualizado! ')
        print()
        print(f"produto: {resultado[0]}")
        print(f"estoque: {resultado[1] - estoque}")
        print()
        conn.close()
        return
    os.system('cls')
    print("produto nao encontrado!")
    conn.close()

def valor_total():
    conn, cursor = conexao()
    cursor.execute("SELECT SUM(preco * quantidade) FROM produtos")
    resultado = cursor.fetchone()
    estoque_total = resultado[0] if resultado[0] is not None else 0
    conn.close()
    print(f"Valor total do estoque: R${estoque_total:.2f}")
    time.sleep(tempo_de_espera)
    return estoque_total
    
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

    opcao = input('Escolha uma opcao: ')
    os.system('cls')

    if opcao == '1':
        cadastro_produto()
        continue

    elif opcao == '2':
        os.system('cls')
        print('===== PRODUTOS =====')
        listar_produtos()
        continue

    elif opcao == '3':
        os.system('cls')
        buscar_produto()
        continue

    elif opcao == '4':
        os.system('cls')
        adicionar_estoque()
        continue

    elif opcao == '5':
        os.system('cls')
        remover_estoque()
        continue

    elif opcao == "6":
        os.system('cls')
        valor_total()
        continue

    elif opcao == '7':
        os.system('cls')
        print('saindo...')
        time.sleep(tempo_de_espera)
        break
