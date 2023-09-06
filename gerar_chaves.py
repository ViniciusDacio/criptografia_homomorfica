import base64

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