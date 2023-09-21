import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os
from tkinter import messagebox

output_directory_cap = 'capturas'

# Crie o diretório se ele não existir
os.makedirs(output_directory_cap, exist_ok=True)

# Variáveis globais
ultimo_frame = None

cap = cv2.VideoCapture(0)  # Captura da webcam (pode variar dependendo da câmera)

# Função para capturar frames da webcam
def capturar_frame():
    global ultimo_frame
    ret, frame = cap.read()

    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ultimo_frame = Image.fromarray(frame)
        imagem = ImageTk.PhotoImage(ultimo_frame)
        label_cam["image"] = imagem
        label_cam.imagem = imagem  # Evitar coleta de lixo
        label_cam.after(10, capturar_frame)

#Pegar nome do usuario
def pegar_nome():
    nome_captura = campo_nome.get()
    if not nome_captura:
        messagebox.showerror("Erro", "Digite um nome de usuário válido.")
        
    return nome_captura

# Função para capturar imagem com um nome específico
def capturar_imagem_com_nome():
    nome = pegar_nome()
    global ultimo_frame
    
    if nome:
        nome_arquivo = f"{nome}.png"
        if ultimo_frame is not None:
            ultimo_frame.save("capturas/"+nome_arquivo)
            #desativar botao
            botao_capturar["state"] = tk.DISABLED
            messagebox.showinfo("Sucesso", f"Imagem capturada como {nome_arquivo}")

'''Interface gráfica'''

# Configuração da janela principal
janela = tk.Tk()
janela.title("Captura de Webcam")

# Configurar grade da janela
janela.columnconfigure(0, weight=1)  # A coluna 0 expande horizontalmente
janela.rowconfigure(0, weight=1)     # A linha 0 expande verticalmente

# Exibição da captura da webcam (ocupando a lateral esquerda)

label_cam = tk.Label(janela)
label_cam.grid(row=0, column=0, sticky="nsew")  # Sticky faz com que o widget ocupe toda a célula

# Frame para os elementos à direita
frame_direita = tk.Frame(janela)
frame_direita.grid(row=0, column=1, padx=10, pady=10)  # Espaçamento para separar da captura

# Campo de entrada para o nome
label_nome = tk.Label(frame_direita, text="Nome:")
label_nome.grid(row=0, column=0)

campo_nome = tk.Entry(frame_direita)
campo_nome.grid(row=0, column=1)

# Botão para capturar imagem
botao_capturar = tk.Button(frame_direita, text="Capturar Imagem", command=capturar_imagem_com_nome)
botao_capturar.grid(row=1, columnspan=2)

# Iniciar a captura de frames da webcam
capturar_frame()

janela.mainloop()

# Liberar a câmera ao fechar a janela
cap.release()
