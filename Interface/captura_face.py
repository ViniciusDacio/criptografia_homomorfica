import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import funcoes
import numpy as np
 
output_directory_cap = 'capturas'

# Crie o diretório se ele não existir
os.makedirs(output_directory_cap, exist_ok=True)
os.makedirs('extracao', exist_ok=True)

# Variáveis globais
ultimo_frame = None
gravando = True
nome_user = None
botao_oculto = None
representacao_facial = None

cap = cv2.VideoCapture(0)  # Captura da webcam (pode variar dependendo da câmera)

# Função para capturar frames da webcam
def capturar_frame():
    global ultimo_frame, gravando

    if gravando:
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
    global nome_user

    nome_user = campo_nome.get()
    if not nome_user:
        messagebox.showerror("Erro", "Digite um nome de usuário válido.")
    else:
        botao_ok["state"] = tk.DISABLED
        campo_nome["state"] = tk.DISABLED
        botao_gera_chaves["state"] = tk.NORMAL
        botao_capturar["state"] = tk.NORMAL
        atualizar_label(label_msg_gera_chaves, "Clique em capturar imagem antes de gerar as chaves.")

# Função para capturar imagem com um nome específico

def pegar_img():
    global gravando, botao_oculto, nome_user

    # Parar a gravação
    gravando = False
    if nome_user and ultimo_frame is not None:

        botao_capturar['text'] = 'Nova Captura'
        botao_capturar['command'] = resetar

        botao_extrair_caracteristicas["state"] = tk.NORMAL

        botao_oculto = tk.Button(frame_direita, text="Salvar", command=salvar_img)
        botao_oculto.grid(row=1, column=2, sticky=tk.E)

def salvar_img():
    global nome_user
    
    nome_arquivo = f"{nome_user}.png"
    ultimo_frame.save("capturas/"+nome_arquivo)
    botao_capturar["state"] = tk.DISABLED
    messagebox.showinfo("Sucesso", f"Imagem capturada como {nome_arquivo}")

#Atualizar texto da label
def atualizar_label(label, texto):
    label["text"] = texto

def resetar():
    global gravando
    global botao_oculto

    # Ativar botão
    botao_capturar["state"] = tk.NORMAL
    botao_capturar["text"] = "Capturar Imagem"
    botao_capturar["command"] = pegar_img

    botao_extrair_caracteristicas["state"] = tk.DISABLED
    botao_oculto.destroy()

    gravando = True
    capturar_frame()

#Chamar função para gerar chaves
def chaves():
    global nome_user

    try:
        funcoes.gerar_chaves(nome_user)
        botao_gera_chaves["state"] = tk.DISABLED
        atualizar_label(label_msg_gera_chaves, "Chaves geradas com sucesso.")
    except:
        atualizar_label(label_msg_gera_chaves, "Erro ao gerar chaves.")

#Chamar função para extrair caracteristicas
def extrair():
    global ultimo_frame, representacao_facial, nome_user

    if ultimo_frame is not None:
        try:
            # Converter o objeto de imagem PIL para um array NumPy
            frame = np.array(ultimo_frame)
            # Chamar a função para extrair características
            representacao_facial= funcoes.extrair_caracteristicas(frame, "extracao/"+nome_user+'_face', True)

            botao_extrair_caracteristicas["state"] = tk.DISABLED
            botao_cifrar["state"] = tk.NORMAL
            botao_capturar["state"] = tk.DISABLED
            atualizar_label(label_msg_caracteristicas, "Características extraídas com sucesso.")
        except:
            atualizar_label(label_msg_caracteristicas, "Erro ao extrair características.")
    else:
        atualizar_label(label_msg_caracteristicas, "Nenhuma imagem capturada para extrair características.")

def cifrar():
    global representacao_facial, nome_user
    
    try:
        funcoes.cifrar(representacao_facial, nome_user, True)
        botao_cifrar["state"] = tk.DISABLED
        atualizar_label(label_msg_cifrar, "Representação facial cifrada com sucesso.")
        messagebox.showinfo("Sucesso", "Processo de Captura Realizada com Sucesso !")
    except:
        atualizar_label(label_msg_cifrar, "Erro ao cifrar representação facial.")

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

campo_nome = tk.Entry(frame_direita, state=tk.NORMAL)
campo_nome.grid(row=0, column=1)

botao_ok = tk.Button(frame_direita, text="OK", command=pegar_nome)
botao_ok.grid(row=0, column=2)

# Botão para capturar imagem
botao_capturar = tk.Button(frame_direita, text="Capturar Imagem",  command=pegar_img, state=tk.DISABLED)
botao_capturar.grid(row=1, columnspan=2, sticky=tk.W)

# Botão para gerar chaves
botao_gera_chaves = tk.Button(frame_direita, text="Gerar chaves", command=chaves, state=tk.DISABLED)
botao_gera_chaves.grid(row=2, columnspan=2)

label_msg_gera_chaves = tk.Label(frame_direita, text="Gere as chaves antes de capturar imagem.")
label_msg_gera_chaves.grid(row=3, columnspan=2)

# Botão para extrair caracteristicas
botao_extrair_caracteristicas = tk.Button(frame_direita, text="Extrair características", command=extrair, state=tk.DISABLED)
botao_extrair_caracteristicas.grid(row=4, columnspan=2)

label_msg_caracteristicas = tk.Label(frame_direita, text="Extraia as características da imagem capturada.")
label_msg_caracteristicas.grid(row=5, columnspan=2)

# Botão para cifrar
botao_cifrar = tk.Button(frame_direita, text="Cifrar", command=cifrar, state=tk.DISABLED)
botao_cifrar.grid(row=6, columnspan=2)

label_msg_cifrar = tk.Label(frame_direita, text="Cifre a representação facial.")
label_msg_cifrar.grid(row=7, columnspan=2)

# Iniciar a captura de frames da webcam
capturar_frame()

janela.mainloop()
cap.release()
