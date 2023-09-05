import cv2
import numpy as np
import os
from tkinter import messagebox
import tkinter as tk

messagebox.showinfo('Data Capture', \
      '- Fique parado para tirar a foto! \n- O programa poderá pedir acesso a camera, prescisamos dela para tirar a foto!')

# Diretório onde as imagens serão armazenadas
output_directory = 'database'

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

        #Tirar foto quando apertar a tecla 's'
        if cv2.waitKey(1) & 0xFF == ord('s'):
            face_image = frame[y:y+h, x:x+w]
            image_name = os.path.join(output_directory, f'capture {len(os.listdir(output_directory)) + 1}.jpg')
            cv2.imwrite(image_name, face_image)

    # Exibe o frame resultante
    cv2.imshow('Face Detection', frame)

    # Sai do loop quando a tecla 'q' é pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a captura de vídeo e fecha a janela
cap.release()
cv2.destroyAllWindows()
