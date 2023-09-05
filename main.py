import tenseal as ts
import gerar_chaves
from deepface import DeepFace

output_directory = 'database'
output_directory = 'chaves'

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

#representação facial (embedding) com Facenet (Deep Learning) para as duas imagens de entrada (img1 e img2)
img1_embedding = DeepFace.represent(img1, model_name = 'Facenet')[0]["embedding"]
img1_embedding = DeepFace.represent(img2, model_name = 'Facenet')[0]["embedding"]

#Criptografia

context = ts.context_from(gerar_chaves.read_data("chaves/secret.txt"))

#criptografar a incorporação da pessoa 1 e 2
enc_v1 = ts.ckks_vector(context, img1_embedding)
enc_v2 = ts.ckks_vector(context, img1_embedding)

#armazenar a incorporação criptografada homomórfica da pessoa 1 e 2
enc_v1_proto = enc_v1.serialize()
enc_v2_proto = enc_v2.serialize()

gerar_chaves.write_data("enc_v1.txt", enc_v1_proto)
gerar_chaves.write_data("enc_v2.txt", enc_v2_proto)

#Calculos

#chave publica
context = ts.context_from(gerar_chaves.read_data("chaves/public.txt"))

#restaurar a incorporação da pessoa 1
enc_v1_proto = gerar_chaves.read_data("enc_v1.txt")
enc_v1 = ts.lazy_ckks_vector_from(enc_v1_proto)
enc_v1.link_context(context)

#restaurar a incorporação da pessoa 1
enc_v2_proto = gerar_chaves.read_data("enc_v2.txt")
enc_v2 = ts.lazy_ckks_vector_from(enc_v2_proto)
enc_v2.link_context(context)

#distancia euclidiana
euclidean_squared = enc_v1 - enc_v2
euclidean_squared = euclidean_squared.dot(euclidean_squared)

#armazenar a distância euclidiana quadrada criptografada homomórfica
gerar_chaves.write_data("euclidean_squared.txt", euclidean_squared.serialize())

#cliente tem a chave secreta
context = ts.context_from(gerar_chaves.read_data("chaves/secret.txt"))

#carregar valor quadrado da distancia euclidiana
euclidean_squared_proto = gerar_chaves.read_data("euclidean_squared.txt")
euclidean_squared = ts.lazy_ckks_vector_from(euclidean_squared_proto)
euclidean_squared.link_context(context)

#descriptografar
euclidean_distance = euclidean_squared.decrypt()[0]

if euclidean_distance < 100:
    print("É a mesma pessoa")
else:
    print("Não é a mesma pessoa")
