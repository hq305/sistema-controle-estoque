import os
import time
import sqlite3

def conexao():
    conn = sqlite3.connect("estoque.db")
    cursor = conn.cursor()
    return conn, cursor

def criar_tabela():
    conn, cursor = conexao()
    cursor.execute('CREATE TABLE IF NOT EXISTS produtos(nome TEXT, preco REAL, quantidade INTEGER)'
                   )
    conn.commit()



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
        return produto,preco,quantidade
        

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
    os.system('cls')
    busca = input("digite o nome do produto: ").strip()
    for i in range(len(produtos)):
        if produtos[i][0].lower() == busca.lower():
            os.system('cls')
            print('produto encontrado!')
            print(f'produto: {produtos[i][0]}')
            print(f'preco: R${produtos[i][1]:.2f}')
            print(f'quantidade: {produtos[i][2]}')
            print()
            time.sleep(tempo_de_espera)
            return
    else:
        os.system('cls')
        print('produto nao encontrado! ')

def adicionar_estoque():
    nome = input('Digite o nome do produto que voce deseja adicionar: ').strip()
    for l in range(len(produtos)):
        if produtos[l][0].lower() == nome.lower():
            os.system('cls')
            print('Produto encontrado!')
            print(f'Produto: {produtos[l][0]}')
            print(f'Estoque atual: {produtos[l][2]}')
            print()
            time.sleep(tempo_de_espera)
            try:
                estoque = int(input('digite a quantidade que deseja adicionar: '))
                if estoque < 0:
                    os.system('cls')
                    print('Quantidade inválida!')
                    return
                produtos[l][2] += estoque
            except ValueError:
                os.system('cls')
                print('Digite um valor valido! ')
                return
            os.system('cls')
            print('estoque atualizado! ')
            print()
            print(f"produto: {produtos[l][0]}")
            print(f"estoque: {produtos[l][2]}")
            print()
            return
    os.system('cls')
    print("produto nao encontrado!")

def remover_estoque():
    nome = input('Digite o nome do produto que voce deseja remover: ').strip()
    for l in range(len(produtos)):
        if produtos[l][0].lower() == nome.lower():
            os.system('cls')
            print('Produto encontrado!')
            print(f'Produto: {produtos[l][0]}')
            print(f'Estoque atual: {produtos[l][2]}')
            print()
            time.sleep(tempo_de_espera)
            try:
                estoque = int(input('digite a quantidade que deseja remover: '))
            except ValueError:
                os.system('cls')
                print('Digite um valor válido!')
                return
            if estoque < 0:
                os.system('cls')
                print('Quantidade inválida!')
                return
            if produtos[l][2] < estoque:
                os.system('cls')
                print('Estoque insuficiente')
                return

            produtos[l][2] -= estoque
            os.system('cls')
            print('estoque atualizado! ')
            print()
            print(f"produto: {produtos[l][0]}")
            print(f"estoque: {produtos[l][2]}")
            print()
            return
    os.system('cls')
    print("produto nao encontrado!")

def valor_total():
    estoque_total = 0
    for l in range(len(produtos)):
        valor = produtos[l][1] * produtos[l][2]
        estoque_total += valor
    print(f"Valor total do estoque: R${estoque_total:.2f}")
    time.sleep(tempo_de_espera)
    return estoque_total
    
        
produtos = []
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
        resultado = cadastro_produto()
        if resultado is None:
            continue
        produto, preco, quantidade = resultado
        for i in range(len(produtos)):
            if produtos[i][0].lower() == produto.lower():
                os.system('cls')
                
                print('produto cadastrado! ')
                time.sleep(tempo_de_espera)
                break
        else:
            conn , cursor = conexao()
            cursor.execute("INSERT INTO produtos VALUES(?, ?, ?)", (produto, preco, quantidade))
            conn.commit()
            
            os.system('cls')
            print("produto cadrastrado! ")
            time.sleep(tempo_de_espera)
            os.system('cls')
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
