import os
from deepface import DeepFace
import tenseal as ts
import util

nome_usuario = "dacio_comparar"

img_biometria = "capturas/"+nome_usuario+".png"

img1_embedding = DeepFace.represent(img_biometria, model_name = 'Facenet')[0]["embedding"]

def cifrar(img1_embedding, chave):
    context = ts.context_from(util.read_data(chave))
    #criptografar a embeddings da pessoa 1
    enc_v1 = ts.ckks_vector(context, img1_embedding)
    #armazenar a embeddings criptografada homomórfica da pessoa 1
    enc_v1_proto = enc_v1.serialize()

    return enc_v1_proto

img_cifrada = cifrar(img1_embedding, "chaves/secret.txt")

#armazenar a embeddings criptografada homomórfica da pessoa 
util.write_data("validacao/"+nome_usuario+".txt", img_cifrada)