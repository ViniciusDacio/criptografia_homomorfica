import dlib
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

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