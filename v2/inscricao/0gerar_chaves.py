import validacao.util as util
import tenseal as ts
import os

def gerar_chaves(caminho):
    context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree = 8192, coeff_mod_bit_sizes = [60, 40, 40, 60])
    context.generate_galois_keys()
    context.global_scale = 2**40

    #gerar chaves secretas
    secret_context = context.serialize(save_secret_key = True)
    util.write_data(caminho+"/secret.txt", secret_context)

    #gerar chaves publicas 
    context.make_context_public() #elimine a secret_key de context
    public_context = context.serialize()
    util.write_data(caminho+"/public.txt", public_context)

output_directory_key = "chaves"
# Crie o diretório se ele não existir
os.makedirs(output_directory_key, exist_ok=True)

gerar_chaves("chaves")
