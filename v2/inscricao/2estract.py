import validacao.util as util
import os
from deepface import DeepFace
import tenseal as ts

nome_usuario = "dacio"

img_biometria = "capturas/"+nome_usuario+".png"

def extrair_caracteristicas(img1, caminho):
    #representação facial (embedding) com Facenet (Deep Learning) para a imagem de entrada
    img1_embedding = DeepFace.represent(img1, model_name = 'Facenet')[0]["embedding"]

    if caminho != None:
        #arquivo com a embeddings(incorporação) da imagem de entrada
        util.gravar_arquivo(caminho, img1_embedding)

output_directory_emb = "inscricao/embedding"
# Crie o diretório se ele não existir
os.makedirs(output_directory_emb, exist_ok=True)

representacao_facial = extrair_caracteristicas(img_biometria, "inscricao/embedding/"+nome_usuario+".txt")