import nacl.secret
import nacl.utils
import gzip #### VERIFICAR USO DE zlib
import zlib
import zipfile
import shutil
import os
import subprocess

key = "LpJkkp01kZPmzoXGltMS5Htb6crspLu/pI7c5EYFzLQ=".decode("base64")
extcrypt = ".crypt"

# This must be kept secret, this is the combination to your safe
# key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
# print "Key: %s" % key
# print "Key base64 encoded: %s" % key.encode("base64")

# This is your safe, you can use it to encrypt or decrypt messages
box = nacl.secret.SecretBox(key)

# This is a nonce, it *MUST* only be used once, but it is not considered
#   secret and can be transmitted or stored alongside the ciphertext. A
#   good source of nonce is just 24 random bytes.
nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
def fencrypt(key, f_plaintext, f_ciphertext, del_input = True):
    with open(f_plaintext, 'rb') as f_in, open(f_ciphertext, 'wb') as f_out:
        plaintext = f_in.read()
        print "Plaintext:", plaintext
        print "Compressing: %d bytes" % len(plaintext)
        plaintext = zlib.compress(plaintext)
        print "Encrypting: %d bytes" % len(plaintext)
        ciphertext = box.encrypt(plaintext, nonce).encode("base64")
        print "Base64 encoded crypto: %d bytes" % len(ciphertext)
        f_out.write(ciphertext)

    if del_input:
        os.remove(f_plaintext)


# VER : http://stackoverflow.com/questions/33178265/write-binary-data-from-a-string-to-a-binary-file

def fdecrypt(key, f_ciphertext, f_plaintext, del_input = True):
    with open(f_ciphertext, 'rb') as f_in, open(f_plaintext, 'wb') as f_out:
        ciphertext = f_in.read().decode("base64")
        print "Decrypting: %d bytes" % len(ciphertext)
        plaintext = box.decrypt(ciphertext)
        print "Uncompressing: %d bytes" % len(plaintext)
        plaintext = zlib.decompress(plaintext)
        print "Plaintext:", plaintext
        f_out.write(plaintext)

    if del_input:
        os.remove(f_ciphertext)


if __name__ == '__main__':
    file_name = 'bdlog.txt'
    fencrypt(key, file_name, file_name + extcrypt)
    fdecrypt(key, file_name + extcrypt, file_name)

