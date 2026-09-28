import tkinter as tk
import sqlite3
from tkinter import messagebox
def conexao():
    conn = sqlite3.connect('dados/estoque.db')
    cursor = conn.cursor()
    return conn, cursor


janela = tk.Tk()
janela.title("Sistema de Estoque")
janela.geometry("300x250")

def cadastrar():
    try:
        produto = campo_produto.get().strip()
        preco = float(campo_preco.get())
        quantidade = int(campo_Quantidade.get())

        if preco < 0:
            messagebox.showerror("Erro" ,"O preço não pode ser negativo")
            campo_preco.delete(0, tk.END)
            return
        if quantidade < 0:
            messagebox.showerror("Erro" ,"A quantidade não pode ser negativa")
            campo_Quantidade.delete(0, tk.END)
            return 
        if not produto:
            messagebox.showerror("Erro" ,"Digite o nome do produto")
            campo_produto.delete(0, tk.END)
            return

    except ValueError:
        messagebox.showerror("Erro" ,"Preço e quantidade precisam ser números")
    else:
        conn, cursor = conexao()
        cursor.execute("SELECT nome FROM produtos WHERE LOWER(nome) = LOWER(?)", (produto,))
        resultado = cursor.fetchone()
        if resultado:
            conn.close()
            messagebox.showwarning('Aviso', "produto ja cadastrado")
        else:
            cursor.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (produto, preco, quantidade))
            conn.commit()
            conn.close()
            messagebox.showinfo('produto','Produto cadastrado com sucesso!')
            campo_produto.delete(0, tk.END)
            campo_Quantidade.delete(0, tk.END)
            campo_preco.delete(0, tk.END)
            
            


rotulo = tk.Label(janela, text="Nome:")
rotulo.pack()
campo_produto = tk.Entry(janela)
campo_produto.pack()


rotulo = tk.Label(janela, text="Preço:")
rotulo.pack()
campo_preco = tk.Entry(janela)
campo_preco.pack()


rotulo = tk.Label(janela, text="Quantidade:")
rotulo.pack()
campo_Quantidade = tk.Entry(janela)
campo_Quantidade.pack()

button = tk.Button(janela, text="cadastrar", command=cadastrar)
button.pack(pady=10)


janela.mainloop()
