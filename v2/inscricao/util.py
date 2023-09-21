import base64
from deepface import DeepFace

def gravar_arquivo(file_name, data):
    with open(file_name, 'w') as arquivo:
        for elemento in data:
            arquivo.write(str(elemento) + '\n')

def write_data(file_name, data):
    if type(data) == bytes:
        #bytes to base64
        data = base64.b64encode(data)
    with open(file_name, 'wb') as f:
        f.write(data)

# Ler chaves
def read_data(file_name):
    with open(file_name, "rb") as f:
        data = f.read()
    #base64 to bytes
    return base64.b64decode(data)

def extrair_caracteristicas(img1, caminho):

    #representação facial (embedding) com Facenet (Deep Learning) para as duas imagens de entrada (img1 e img2)
    img1_embedding = DeepFace.represent(img1, model_name = 'Facenet')[0]["embedding"]

    if caminho != None:
        #arquivos com as embeddings(incorporação) das duas imagens de entrada (img1 e img2)
        gravar_arquivo(caminho, img1_embedding)

    return img1_embedding