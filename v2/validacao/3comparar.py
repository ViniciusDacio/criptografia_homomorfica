import util
import tenseal as ts
from deepface import DeepFace
from tkinter import messagebox

chave_privada = "chaves/secret.txt"
chave_publica = "chaves/public.txt"

context = ts.context_from(util.read_data(chave_publica))

arq1 = util.read_data("database/dacio_cifrado.txt")
arq_base = ts.lazy_ckks_vector_from(arq1)
arq_base.link_context(context)

arq2 = util.read_data("validacao/dacio_comparar.txt")
arq_validacao = ts.lazy_ckks_vector_from(arq2)
arq_validacao.link_context(context)

#comparar dois vetores criptografados homomorficamente
def comparacao(enc_v1, enc_v2, chave):
    #distancia euclidiana
    euclidean_squared = enc_v1 - enc_v2
    euclidean_squared = euclidean_squared.dot(euclidean_squared)

    #armazenar a distância euclidiana quadrada criptografada homomórfica
    util.write_data("euclidean_squared.txt", euclidean_squared.serialize())

    #cliente tem a chave secreta
    context = ts.context_from(util.read_data(chave))

    #carregar valor quadrado da distancia euclidiana
    euclidean_squared_proto = util.read_data("euclidean_squared.txt")
    euclidean_squared = ts.lazy_ckks_vector_from(euclidean_squared_proto)
    euclidean_squared.link_context(context)

    #descriptografar
    euclidean_distance = euclidean_squared.decrypt()[0]

    if euclidean_distance < 100:
        messagebox.showinfo("Sucesso", "Usuário reconhecido!")
    else:
        messagebox.showerror("Erro", "Usuário não reconhecido!")

comparacao(arq_base, arq_validacao, chave_privada)
