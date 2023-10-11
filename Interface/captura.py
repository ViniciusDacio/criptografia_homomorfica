import tkinter as tk
from tkinter import ttk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import os
from tkinter import messagebox, filedialog
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
webcam_disponivel = True
salvar_arq = True
usuario_comparar = None

cap = cv2.VideoCapture(0)  # Captura da webcam (pode variar dependendo da câmera)

# Função para capturar frames da webcam
def capturar_frame():
    global ultimo_frame, gravando
    #janela.geometry("1280x480")

    if gravando:
        ret, frame = cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ultimo_frame = Image.fromarray(frame)
            imagem = ImageTk.PhotoImage(ultimo_frame)
            label_cam["image"] = imagem
            label_cam.imagem = imagem  # Evitar coleta de lixo
            label_cam.after(10, capturar_frame)
    else:
     # Se a captura da webcam falhar, exiba uma imagem em branco e a mensagem
        imagem_branca = Image.new("RGB", (640, 480), (255, 255, 255))
        label_cam["image"] = imagem_branca
        label_cam.imagem = imagem_branca
        webcam_disponivel = False

        label_cam.after(1000, capturar_frame)  # Tente novamente após 1 segundo

#Pegar nome do usuario
def pegar_nome():
    global nome_user

    nome_user = campo_nome.get()
    if not nome_user:
        messagebox.showerror("Erro", "Digite um nome de usuário válido.")
    elif funcoes.arquivo_existe('extracao/'+nome_user+'_cifrado.txt') :
        messagebox.showerror("Erro", "Usuário já cadastrado.")
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

        botao_oculto = tk.Button(frame_valida, text="Salvar", command=salvar_img)
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
        representacao_facial = None
        atualizar_label(label_msg_cifrar, "Representação facial cifrada com sucesso.")
        messagebox.showinfo("Sucesso", "Processo de Captura Realizada com Sucesso !")
    except:
        atualizar_label(label_msg_cifrar, "Erro ao cifrar representação facial.")

def exibir_texto(texto, frame, label):
    # Crie um widget de texto
    text_widget = Text(frame)
    text_widget.pack()

    # Abra o arquivo em modo de leitura ('r')
    with open(texto, 'r') as file:
        # Leia o conteúdo do arquivo
        conteudo = file.read()

    # Insira o conteúdo do arquivo no widget de texto
    text_widget.insert('end', conteudo)
    label["text"] = text_widget

#buscar dados do usuario
def buscar():
    global ultimo_frame
    nome = campo_busca_nome.get()

    if funcoes.arquivo_existe('extracao/'+nome+'_cifrado.txt') :
        ultimo_frame = None
        botao_busca["state"] = tk.DISABLED
        botao_capturar2["state"] = tk.NORMAL
        messagebox.showinfo("Sucesso", "Usuario "+nome+ " encontrado !")
    else:
        messagebox.showinfo("Erro", "Usuario "+nome+" não encontrado !")

def pegar_img_autencicacao():
    global gravando, botao_oculto, salvar_arq

    salvar_arq = False
    # Parar a gravação
    gravando = False
    if ultimo_frame is not None:

        botao_capturar2['text'] = 'Nova Captura'
        botao_capturar2['command'] = resetar

        botao_extrair_caracteristicas2["state"] = tk.NORMAL

def extrair_aut():
    global ultimo_frame, representacao_facial, nome_user, salvar_arq
    nome_user = campo_busca_nome.get()

    if ultimo_frame is not None:
        try:
            # Converter o objeto de imagem PIL para um array NumPy
            frame = np.array(ultimo_frame)
            # Chamar a função para extrair características
            representacao_facial= funcoes.extrair_caracteristicas(frame, "extracao/"+nome_user+'_face', False)

            botao_extrair_caracteristicas2["state"] = tk.DISABLED
            botao_cifrar2["state"] = tk.NORMAL
            botao_capturar2["state"] = tk.DISABLED
            campo_busca_nome["state"] = tk.DISABLED
            atualizar_label(label_msg_caracteristicas2, "Características extraídas com sucesso.")
        except:
            atualizar_label(label_msg_caracteristicas2, "Erro ao extrair características.")
    else:
        atualizar_label(label_msg_caracteristicas2, "Nenhuma imagem capturada para extrair características.")

def cifrar_aut():
    global representacao_facial, nome_user, usuario_comparar
    nome_user = campo_busca_nome.get()
    
    try:
        usuario_comparar = funcoes.cifrar(representacao_facial, nome_user, False)
        botao_cifrar2["state"] = tk.DISABLED
        botao_comparar["state"] = tk.NORMAL
        atualizar_label(label_msg_cifrar2, "Representação facial cifrada com sucesso.")
    except:
        atualizar_label(label_msg_cifrar2, "Erro ao cifrar representação facial.")

def comparar():
    global nome_user, usuario_comparar
    nome_user = campo_busca_nome.get()

    arq_base, arq_validacao = funcoes.deserializar(nome_user, usuario_comparar, 'chaves/'+nome_user+'_public.txt')
    resultado = funcoes.comparacao(arq_base, arq_validacao, 'chaves/'+nome_user+'_secret.txt')

    if resultado < 100:
        messagebox.showinfo("Sucesso", "Usuário reconhecido! %.2f" % resultado)
    else:
        messagebox.showerror("Erro", "Usuário não reconhecido! %.2f" % resultado)
    botao_comparar["state"] = tk.DISABLED
    
'''Interface gráfica'''

# Configuração da janela principal
janela = tk.Tk()
janela.title("Captura de Webcam")

# Divide a janela em dois frames: esquerdo e direito
frame_esquerdo = tk.Frame(janela, width=200, height=200)
frame_esquerdo.pack(side="left", expand=True, fill="both")

frame_direito = tk.Frame(janela)
frame_direito.pack(side="right", expand=True, fill="both")

# Cria um notebook (para abas) no frame direito
tabs = ttk.Notebook(frame_direito)

# Cria duas abas: uma para a captura e outra para a captura/verificação
frame_valida = ttk.Frame(tabs)
frame_autentica = ttk.Frame(tabs)

tabs.add(frame_valida, text="Inscrição")
tabs.add(frame_autentica, text="Autenticação")

tabs.pack(fill=BOTH, expand=TRUE)

#Inicializa a captura de frames


# Configure the grid weights
frame_valida.grid_columnconfigure(0, weight=4)
frame_valida.grid_columnconfigure(1, weight=1)

# Exibição da captura da webcam
label_cam = tk.Label(frame_esquerdo)
label_cam.grid(row=0, column=0, sticky="nsew")  # Sticky faz com que o widget ocupe toda a célula

# Frame para os elementos à direita
frame_valida = tk.Frame(frame_valida)
frame_valida.grid(row=0, column=1, padx=10, pady=10)  # Espaçamento para separar da captura

# Campo de entrada para o nome
label_nome = tk.Label(frame_valida, text="Nome:")
label_nome.grid(row=0, column=0)

campo_nome = tk.Entry(frame_valida, state=tk.NORMAL)
campo_nome.grid(row=0, column=1)

botao_ok = tk.Button(frame_valida, text="OK", command=pegar_nome)
botao_ok.grid(row=0, column=2)

# Botão para capturar imagem
botao_capturar = tk.Button(frame_valida, text="Capturar Imagem",  command=pegar_img, state=tk.DISABLED)
botao_capturar.grid(row=1, columnspan=2, sticky=tk.W)

# Botão para gerar chaves
botao_gera_chaves = tk.Button(frame_valida, text="Gerar chaves", command=chaves, state=tk.DISABLED)
botao_gera_chaves.grid(row=2, columnspan=2)

label_msg_gera_chaves = tk.Label(frame_valida, text="Gere as chaves antes de capturar imagem.")
label_msg_gera_chaves.grid(row=3, columnspan=2)

# Botão para extrair caracteristicas
botao_extrair_caracteristicas = tk.Button(frame_valida, text="Extrair características", command=extrair, state=tk.DISABLED)
botao_extrair_caracteristicas.grid(row=4, columnspan=2)

label_msg_caracteristicas = tk.Label(frame_valida, text="Extraia as características da imagem capturada.")
label_msg_caracteristicas.grid(row=5, columnspan=2)

# Botão para cifrar
botao_cifrar = tk.Button(frame_valida, text="Cifrar", command=cifrar, state=tk.DISABLED)
botao_cifrar.grid(row=6, columnspan=2)

label_msg_cifrar = tk.Label(frame_valida, text="Cifre a representação facial.")
label_msg_cifrar.grid(row=7, columnspan=2)

'''Frame Autenticação'''

# Configure the grid weights
frame_autentica.grid_columnconfigure(0, weight=4)
frame_autentica.grid_columnconfigure(1, weight=1)

# Exibição da captura da webcam
label_cam2 = tk.Label(frame_autentica)
label_cam2.grid(row=0, column=0, sticky="nsew")  # Sticky faz com que o widget ocupe toda a célula

# Frame para os elementos à direita
frame_autentica = tk.Frame(frame_autentica)
frame_autentica.grid(row=0, column=1, padx=10, pady=10) 

#Buscar nome do usuario
label_busca_nome = tk.Label(frame_autentica, text="Nome:")
label_busca_nome.grid(row=0, column=0)

campo_busca_nome = tk.Entry(frame_autentica, state=tk.NORMAL)
campo_busca_nome.grid(row=0, column=1)

# Botão para buscar
botao_busca = tk.Button(frame_autentica, text="Buscar", command=buscar)
botao_busca.grid(row=0, column=2)

# Botão para capturar imagem
botao_capturar2 = tk.Button(frame_autentica, text="Capturar Imagem",  command=pegar_img_autencicacao, state=tk.DISABLED)
botao_capturar2.grid(row=1, columnspan=2, sticky=tk.W)

# Botão para extrair caracteristicas
botao_extrair_caracteristicas2 = tk.Button(frame_autentica, text="Extrair características", command=extrair_aut, state=tk.DISABLED)
botao_extrair_caracteristicas2.grid(row=4, columnspan=2)

label_msg_caracteristicas2 = tk.Label(frame_autentica, text="Extraia as características da imagem capturada.")
label_msg_caracteristicas2.grid(row=5, columnspan=2)

# Botão para cifrar
botao_cifrar2 = tk.Button(frame_autentica, text="Cifrar", command=cifrar_aut, state=tk.DISABLED)
botao_cifrar2.grid(row=6, columnspan=2)

label_msg_cifrar2 = tk.Label(frame_autentica, text="Cifre a representação facial.")
label_msg_cifrar2.grid(row=7, columnspan=2)

# Botão para copmparar
botao_comparar = tk.Button(frame_autentica, text="Comparar", command=comparar, state=tk.DISABLED)
botao_comparar.grid(row=8, columnspan=2)

label_msg_comparar = tk.Label(frame_autentica, text="Comparar a representação facial.")
label_msg_comparar.grid(row=9, columnspan=2)

# Iniciar a captura de frames da webcam
capturar_frame()

janela.mainloop()
cap.release()