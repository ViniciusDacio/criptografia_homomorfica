import tenseal as ts
import gerar_chaves
from deepface import DeepFace
import os

output_directory_data = 'database'
output_directory_key = 'chaves'
output_directory_features = 'features'
output_directory_cifra = 'cifrado'

# Crie o diretório se ele não existir
os.makedirs(output_directory_data, exist_ok=True)
os.makedirs(output_directory_key, exist_ok=True)
os.makedirs(output_directory_features, exist_ok=True)
os.makedirs(output_directory_cifra, exist_ok=True)

def gravar_arquivo(file_name, data):
    with open(file_name, 'w') as arquivo:
        for elemento in data:
            arquivo.write(str(elemento) + '\n')

#gerar chaves
context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree = 8192, coeff_mod_bit_sizes = [60, 40, 40, 60])
context.generate_galois_keys()
context.global_scale = 2**40

#gerar chaves secretas
secret_context = context.serialize(save_secret_key = True)
gerar_chaves.write_data("chaves/secret.txt", secret_context)

#gerar chaves publicas 
context.make_context_public() #elimine a secret_key de context
public_context = context.serialize()
gerar_chaves.write_data("chaves/public.txt", public_context) 

img1 = "database/face_1.jpg"
img2 = "database/face_2.jpg"

'''Extrtação de caracteristicas'''

#representação facial (embedding) com Facenet (Deep Learning) para as duas imagens de entrada (img1 e img2)
img1_embedding = DeepFace.represent(img1, model_name = 'Facenet')[0]["embedding"]
img2_embedding = DeepFace.represent(img2, model_name = 'Facenet')[0]["embedding"]

#arquivos com as embeddings(incorporação) das duas imagens de entrada (img1 e img2)
gravar_arquivo("features/img1_features.txt", img1_embedding)
gravar_arquivo("features/img2_features.txt", img2_embedding)

'''Criptografia'''

context = ts.context_from(gerar_chaves.read_data("chaves/secret.txt"))

#criptografar a embeddings da pessoa 1 e 2
enc_v1 = ts.ckks_vector(context, img1_embedding)
enc_v2 = ts.ckks_vector(context, img2_embedding)

#armazenar a embeddings criptografada homomórfica da pessoa 1 e 2
enc_v1_proto = enc_v1.serialize()
enc_v2_proto = enc_v2.serialize()

gerar_chaves.write_data("cifrado/enc_v1.txt", enc_v1_proto)
gerar_chaves.write_data("cifrado/enc_v2.txt", enc_v2_proto)

#distancia euclidiana
euclidean_squared = enc_v1 - enc_v2
euclidean_squared = euclidean_squared.dot(euclidean_squared)

#armazenar a distância euclidiana quadrada criptografada homomórfica
gerar_chaves.write_data("cifrado/euclidean_squared.txt", euclidean_squared.serialize())

#cliente tem a chave secreta
context = ts.context_from(gerar_chaves.read_data("chaves/secret.txt"))

#carregar valor quadrado da distancia euclidiana
euclidean_squared_proto = gerar_chaves.read_data("cifrado/euclidean_squared.txt")
euclidean_squared = ts.lazy_ckks_vector_from(euclidean_squared_proto)
euclidean_squared.link_context(context)

#descriptografar
euclidean_distance = euclidean_squared.decrypt()[0]

#Descriptografar a embeddings da pessoa 1
m_proto = gerar_chaves.read_data("cifrado/enc_v1.txt")
m = ts.lazy_ckks_vector_from(m_proto)
m.link_context(context)
descrypt = m.decrypt()
gravar_arquivo("features/img1_descrypt.txt", descrypt)

if euclidean_distance < 100:
    print("É a mesma pessoa")
else:
    print("Não é a mesma pessoa")
