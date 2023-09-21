import util
import tenseal as ts

img_biometria = "capturas/dacio.png"
nome_usuario = "dacio"

representacao_facial = util.extrair_caracteristicas(img_biometria, "inscricao/embedding/"+nome_usuario+".txt")

def cifra(img1_embedding, chave):
    context = ts.context_from(util.read_data(chave))
    #criptografar a embeddings da pessoa 1
    enc_v1 = ts.ckks_vector(context, img1_embedding)
    #armazenar a embeddings criptografada homomórfica da pessoa 1
    enc_v1_proto = enc_v1.serialize()

    return enc_v1_proto

img_cifrada = cifra(representacao_facial, "chaves/secret.txt")

#armazenar a embeddings criptografada homomórfica da pessoa 
util.write_data("database/"+nome_usuario+"_cifrado.txt", img_cifrada)
