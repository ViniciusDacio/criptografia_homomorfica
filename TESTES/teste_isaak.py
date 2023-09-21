import cv2
import tkinter as tk
from tkinter import messagebox
import os
import threading
import time
import dlib
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Função para atualizar o rótulo com a mensagem
def atualizar_mensagem(mensagem):
    label_mensagem.config(text=mensagem)

# Função para mostrar a mensagem de espera por 4 segundos
def mostrar_mensagem_espera():
    mensagem_espera = "Aguarde sua captura está sendo processada..."
    atualizar_mensagem(mensagem_espera)
    time.sleep(4)
    atualizar_mensagem("Sua captura foi concluída.")

# Função para tirar a foto e salvar com o nome inserido pelo usuário
def capturar_face():
    nome_usuario = entrada_nome.get()
    
    if not nome_usuario:
        messagebox.showerror("Erro", "Digite um nome de usuário válido.")
        return
    
    # Atualizar a mensagem na interface
    atualizar_mensagem("Sua face está sendo capturada e analisada...")
    
    # Diretório onde as imagens serão armazenadas
    output_directory = 'capturas'
    
    # Crie o diretório se ele não existir
    os.makedirs(output_directory, exist_ok=True)
    
    # Inicializa a captura de vídeo
    cap = cv2.VideoCapture(0)
    
    # Carrega o classificador de detecção de faces
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    while True:
        # Captura um frame da câmera
        ret, frame = cap.read()
        
        # Converte o frame para tons de cinza para a detecção de faces funcionar melhor
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        # Detecta faces no frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    
        # Desenha um retângulo ao redor de cada face detectada
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
            # Capturar a foto quando a tecla 's' é pressionada
            if cv2.waitKey(1) & 0xFF == ord('s'):
                face_image = frame[y:y+h, x:x+w]
                image_name = os.path.join(output_directory, f'{nome_usuario}_capture_{len(os.listdir(output_directory)) + 1}.jpg')
                cv2.imwrite(image_name, face_image)
                mensagem = f"Sua face foi capturada e está sendo analisada. Salva como {image_name}."

                atualizar_mensagem(mensagem)
                cap.release()
                cv2.destroyAllWindows()

                # Iniciar a thread para mostrar a mensagem de espera
                espera_thread = threading.Thread(target=mostrar_mensagem_espera)
                espera_thread.start()
                return
    
        # Exibe o frame resultante
        cv2.imshow('Face Detection', frame)
    
        # Sai do loop quando a tecla 'q' é pressionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
        # Carrega o classificador de detecção de faces
detector = dlib.get_frontal_face_detector()

# Carrega o classificador de reconhecimento facial
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Cria o fuzzy vault
fuzzy_vault = []

# Define a chave secreta
key = b'mysecretkey12345'

# Captura a imagem da câmera
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

# Detecta a face na imagem
faces = detector(frame)

# Extrai as características faciais da face detectada
for face in faces:
    landmarks = predictor(frame, face)
    features = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(68)])
    
    # Adiciona as características faciais ao fuzzy vault
    fuzzy_vault.append(features)

# Protege o fuzzy vault usando criptografia
cipher = AES.new(key, AES.MODE_CBC)
encrypted_vault = cipher.encrypt(pad(str(fuzzy_vault).encode('utf-8'), AES.block_size))

# Salva o fuzzy vault criptografado em um arquivo
with open('fuzzy_vault.bin', 'wb') as f:
    f.write(encrypted_vault)