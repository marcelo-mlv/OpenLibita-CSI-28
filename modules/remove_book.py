from tkinter import *
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image
import backend

def remove_book(main_frame):
    """
    Displays a list of current books and allows the user to remove a selected book.
    """
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Configuração das colunas para distribuição de espaço uniforme
    for i in range(9):  # Supondo que o layout usa 9 colunas
        main_frame.grid_columnconfigure(i, weight=1)

    # Canvas para rolagem horizontal
    canvas = Canvas(main_frame)
    canvas.grid(row=0, column=0, columnspan=9, padx=80, pady=(120, 10), sticky="nsew")

    # Frame interno que será rolado
    scrollable_frame = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Barra de rolagem horizontal
    h_scroll = Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
    h_scroll.grid(row=1, column=0, columnspan=9, padx=80, sticky="ew")
    canvas.configure(xscrollcommand=h_scroll.set)

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", update_scrollregion)

    def submit_removal():
        book_id = book_id_entry.get()

        if not book_id:
            messagebox.showerror("Erro", "ID do livro é obrigatório.")
            return

        if book_id not in [str(book[0]) for book in books]:
            messagebox.showerror("Erro", "ID de Livro não encontrado.")
            return

        result = backend.remove_book(book_id)
        if isinstance(result, str):
            if result == "Indisponível":
                messagebox.showerror("Erro", "Esse livro não pode ser removido pois está sendo emprestado.")
            else:
                messagebox.showerror("Erro", result)
        else:
            messagebox.showinfo("Sucesso", "Livro removido com sucesso.")
            restore_mainframe(main_frame)

    def restore_mainframe(main_frame):
        for widget in main_frame.winfo_children():
            widget.destroy()
        imagem_principal = ctk.CTkImage(light_image=Image.open("assets\\imagemFramePrincipal.jpeg"), size=(500, 500))
        label_imagem_principal = ctk.CTkLabel(master=main_frame, image=imagem_principal, text="")
        label_imagem_principal.place(relx=0.5, rely=0.5, anchor="center")
        label_citacao = ctk.CTkLabel(
            master=main_frame,
            text="“A educação é a arma mais poderosa que você pode usar para mudar o mundo”\nNelson Mandela",
            font=("Roboto", 16, 'italic'),
            text_color="black",
            justify="left"
        )
        label_citacao.pack(side="bottom", padx=20, pady=20, anchor="se")

    books, columns = backend.get_books()
    if isinstance(books, str):
        messagebox.showerror("Erro", books)
        restore_mainframe(main_frame)
        return

    if not books:
        messagebox.showinfo("Info", "Nenhum livro encontrado no banco de dados.")
        restore_mainframe(main_frame)
        return
    
    page_index = 0
    books_per_page = 10

    def display_books():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        i = 0
        for col in columns:
            col_label = ctk.CTkLabel(master=scrollable_frame, text=col, font=("Roboto", 12, 'bold'))
            col_label.grid(row=0, column=i, padx=5, pady=2, sticky='w')
            scrollable_frame.grid_columnconfigure(i, weight=1)  # Configuração das colunas do scrollable_frame
            i += 1

        current_page_books = books[books_per_page * page_index: books_per_page * (page_index + 1)]
        i = 1
        for book in current_page_books:
            j = 0
            formatted_book = (
                book[0],
                book[1],
                book[2],
                book[3],
                book[4],
                "Sim" if book[5] else "Não",  # Loan status
                book[7],
                book[8],
                book[9],
            )
            for value in formatted_book:
                value_label = ctk.CTkLabel(master=scrollable_frame, text=value)
                value_label.grid(row=i, column=j, padx=5, pady=2)
                j += 1
            i += 1

        previous_page_button.configure(state="normal" if page_index > 0 else "disabled")
        next_page_button.configure(state="normal" if books_per_page * (page_index + 1) < len(books) else "disabled")

    def next_page():
        nonlocal page_index
        page_index += 1
        display_books()

    def previous_page():
        nonlocal page_index
        page_index -= 1
        display_books()

    previous_page_button = ctk.CTkButton(
        main_frame, 
        text="Página Anterior", 
        font=("Roboto", 14, 'bold'),
        fg_color="#98a164",
        hover_color="#5c613e",
        text_color="#FFFFFF",
        corner_radius=2,
        border_width=1,
        border_color="#585c45",
        command=previous_page
    )
    previous_page_button.grid(row=2, column=0, padx=(80, 10), pady=10, sticky="w")

    next_page_button = ctk.CTkButton(
        main_frame, 
        text="Próxima Página", 
        font=("Roboto", 14, 'bold'),
        fg_color="#98a164",
        hover_color="#5c613e",
        text_color="#FFFFFF",
        corner_radius=2,
        border_width=1,
        border_color="#585c45",
        command=next_page
    )
    next_page_button.grid(row=2, column=8, padx=(10, 80), pady=10, sticky="e")

    display_books()

    ctk.CTkLabel(main_frame, text="ID do Empréstimo:", font=("Roboto", 14)).grid(row=3, column=0, padx=(80, 0), pady=(20, 5), sticky='w')
    book_id_entry = ctk.CTkEntry(main_frame, placeholder_text="Digite o ID do Empréstimo", fg_color="#E0DFDF", corner_radius=2, border_color="#c2c0c0", border_width=1)
    book_id_entry.grid(row=3, column=1, pady=(20, 5), sticky='w')

    ctk.CTkButton(
        main_frame, 
        text="Concluir Devolução", 
        font=("Roboto", 14, 'bold'),
        fg_color="#98a164",
        hover_color="#5c613e",
        text_color="#FFFFFF",
        corner_radius=2,
        border_width=1,
        border_color="#585c45",
        command=submit_removal
    ).grid(row=4, column=0, columnspan=9, padx=(160, 160), pady=20, sticky="ew")
