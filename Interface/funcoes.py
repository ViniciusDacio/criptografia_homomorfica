import tenseal as ts
from deepface import DeepFace
import base64
import os

# Crie o diretório se ele não existir
os.makedirs('chaves', exist_ok=True)
os.makedirs('extracao', exist_ok=True)

# Gerar chaves
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

def gravar_arquivo(file_name, data):
    with open(file_name, 'w') as arquivo:
        for elemento in data:
            arquivo.write(str(elemento) + '\n')

def gerar_chaves(nome_arq):
    context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree = 8192, coeff_mod_bit_sizes = [60, 40, 40, 60])
    context.generate_galois_keys()
    context.global_scale = 2**40

    #gerar chaves secretas
    secret_context = context.serialize(save_secret_key = True)
    write_data('chaves/'+nome_arq+'_secret.txt', secret_context)

    #gerar chaves publicas 
    context.make_context_public() #elimine a secret_key de context
    public_context = context.serialize()
    write_data('chaves/'+nome_arq+'_public.txt', public_context)

def extrair_caracteristicas(img1, caminho, salvar):

    #representação facial (embedding) com Facenet (Deep Learning) para as duas imagens de entrada (img1 e img2)
    img1_embedding = DeepFace.represent(img1, model_name = 'Facenet')[0]["embedding"]

    if salvar == True:
        #arquivos com as embeddings(incorporação) das duas imagens de entrada (img1 e img2)
        gravar_arquivo(caminho, img1_embedding)

    return img1_embedding

def cifrar(img1_embedding, nome_arq, salvar):
    context = ts.context_from(read_data("chaves/"+nome_arq+"_secret.txt"))

    #criptografar a embeddings da pessoa 1 e 2
    enc_v1 = ts.ckks_vector(context, img1_embedding)

    #armazenar a embeddings criptografada homomórfica da pessoa 1 e 2
    enc_v1_proto = enc_v1.serialize()
    if salvar == True:
        write_data("extracao/"+nome_arq+"_cifrado.txt", enc_v1_proto)
    return enc_v1_proto

def deserializar(usuario_base, arq_cifra, chave_publica):
    context = ts.context_from(read_data(chave_publica))

    arq1 = read_data("extracao/"+usuario_base+"_cifrado.txt")
    arq_base = ts.lazy_ckks_vector_from(arq1)
    arq_base.link_context(context)

    arq_validacao = ts.lazy_ckks_vector_from(arq_cifra)
    arq_validacao.link_context(context)

    return arq_base, arq_validacao

def comparacao(enc_v1, enc_v2, chave):
    euclidean_squared = enc_v1 - enc_v2
    euclidean_squared = euclidean_squared.dot(euclidean_squared)

    #armazenar a distância euclidiana quadrada criptografada homomórfica
    write_data("euclidean_squared.txt", euclidean_squared.serialize())

    #cliente tem a chave secreta
    context = ts.context_from(read_data(chave))

    #carregar valor quadrado da distancia euclidiana
    euclidean_squared_proto = read_data("euclidean_squared.txt")
    euclidean_squared = ts.lazy_ckks_vector_from(euclidean_squared_proto)
    euclidean_squared.link_context(context)

    #descriptografar resultado
    euclidean_distance = euclidean_squared.decrypt()[0]

    return euclidean_distance

def arquivo_existe(caminho):
    return os.path.isfile(caminho)
