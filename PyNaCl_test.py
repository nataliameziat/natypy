import nacl.secret
import nacl.utils
import gzip #### VERIFICAR USO DE zlib
import zlib
import shutil

file_name = 'bdlog.txt.gz'

# This must be kept secret, this is the combination to your safe
key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)

# This is your safe, you can use it to encrypt or decrypt messages
box = nacl.secret.SecretBox(key)

# This is a nonce, it *MUST* only be used once, but it is not considered
#   secret and can be transmitted or stored alongside the ciphertext. A
#   good source of nonce is just 24 random bytes.
nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

# Apenas compacta
with open(file_name, 'rb') as f_in, open(file_name + '.crypt', 'wb') as f_out:
    # LER f_in e criptografar o conteúdo, depois escrever o conteúdo criptografado em f_out
    shutil.copyfileobj(cypher_data, f_out)
    #shutil.copyfileobj(f_in, f_out)


# This is our message to send, it must be a bytestring as SecretBox will
#   treat is as just a binary blob of data.
# Read the entire file as a single byte string
with open(file_name, 'rb') as f:
    message = f.read()

# Encrypt our message, it will be exactly 40 bytes longer than the original
#   message as it stores authentication information and nonce alongside it.
encrypted = box.encrypt(message, nonce)

# Decrypt our message, an exception will be raised if the encryption was
#   tampered with or there was otherwise an error.
#plaintext = box.decrypt(encrypted)

# Write binary data to a file
with open(file_name + '.crypt', 'wb') as f:
    f.write(encrypted)

# VER : http://stackoverflow.com/questions/33178265/write-binary-data-from-a-string-to-a-binary-file