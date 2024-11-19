from tkinter import *
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import backend
from datetime import datetime
from modules.common import LabelEntry, SubmitButton

def add_loan(frame_principal):
    """
    Modifica o frame_principal para exibir campos de digitação para um novo empréstimo.

    Args:
        frame_principal: O frame principal onde o conteúdo será exibido.
    """
    # Limpa o conteúdo atual do frame_principal
    for widget in frame_principal.winfo_children():
        widget.destroy()

    # Cria widgets de entrada e botões no frame_principal
    def submit_loan():
        id_usuario = id_usuario_entry.get()
        id_livro = id_livro_entry.get()
        data_emprestimo = data_emprestimo_entry.get()
        data_prevista_devolucao = data_prevista_devolucao_entry.get()

        if not id_usuario or not id_livro or not data_emprestimo or not data_prevista_devolucao:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return
        
        try:
            # Ensure the dates are in the correct format
            data_emprestimo = datetime.strptime(data_emprestimo, '%d/%m/%Y').strftime('%Y-%m-%d')
            data_prevista_devolucao = datetime.strptime(data_prevista_devolucao, '%d/%m/%Y').strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erro", "Datas inválidas. Use o formato DD/MM/AAAA.")
            return

        result = backend.add_loan(id_usuario, id_livro, data_emprestimo, data_prevista_devolucao)
        if isinstance(result, str):
            messagebox.showerror("Erro", result)
        else:
            messagebox.showinfo("Sucesso", "Empréstimo adicionado com sucesso.")
            restaurar_frame_principal(frame_principal)  # Restaura o frame original após o envio

    # Cria função para restaurar o frame_principal com a imagem e citação
    def restaurar_frame_principal(frame_principal):
        for widget in frame_principal.winfo_children():
            widget.destroy()
        imagem_principal = ctk.CTkImage(light_image=Image.open("assets\\imagemFramePrincipal.jpeg"), size=(500, 500))
        label_imagem_principal = ctk.CTkLabel(master=frame_principal, image=imagem_principal, text="")
        label_imagem_principal.place(relx=0.5, rely=0.5, anchor="center")

        label_citacao = ctk.CTkLabel(
            master=frame_principal,
            text="“A educação é a arma mais poderosa que você pode usar para mudar o mundo”\nNelson Mandela",
            font=("Roboto", 16, 'italic'),
            text_color="black",
            justify="left"
        )
        label_citacao.pack(side="bottom", padx=20, pady=20, anchor="se")

    
    # Configuração dos campos de entrada com grid
    id_livro_entry = LabelEntry(frame_principal, "ID do Livro", 0, 0, (120, 0), (120, 5), (120, 0), 10)
    id_usuario_entry = LabelEntry(frame_principal, "ID do Aluno", 0, 2, 10, (120, 5), 10, 10)
    data_emprestimo_entry = LabelEntry(frame_principal, "Data do Empréstimo", 2, 0, (120, 0), (10, 5), (120, 0), (0,10))
    data_prevista_devolucao_entry = LabelEntry(frame_principal, "Previsão de Devolução", 2, 2, 10, 10, 10, 10)

    SubmitButton(frame_principal, "Realizar Empréstimo", submit_loan, 4, 0, 3, (120, 0), 40, sticky=EW)

    # Expande as colunas 1 e 3 para que os campos de entrada possam crescer horizontalmente
    frame_principal.grid_columnconfigure(1, weight=1)
    frame_principal.grid_columnconfigure(3, weight=1)
