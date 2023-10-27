from base64 import b64decode, b64encode
from operator import indexOf
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES
from Crypto.Cipher import ARC4
from Crypto.Hash import SHA
from Crypto.Signature import pkcs1_15
import socket
import json


def aes_encryption(data):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    nonce = cipher.nonce
    return key, cipher, ciphertext, tag, nonce

def aes_decryption(key, nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    return data

def rsa_encryption(data):
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
    ciphertext = cipher.encrypt(data)
    return private_key, public_key, cipher, ciphertext

def rsa_decryption(private_key, ciphertext):
    cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
    data = cipher.decrypt(ciphertext)
    return data

def socket_listener():
    host = '0.0.0.0'  # Listen on all available network interfaces
    port = 55555  # Use an available port number    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Listen for up to 5 incoming connections
    print(f"Listening on {host}:{port}")
    while True: 
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
         # Handle incoming data
        data = client_socket.recv(1024)  # Receive up to 1024 bytes of data
        if not data:
            print("no data found")
            break  # If no data is received, exit the loop
        print(f"Received data: {data.decode('utf-8')}")
        response = "Data received successfully\n"
        client_socket.send(response.encode('utf-8'))
        # Close the client socket
        client_socket.close()
    # Close the server socket when done
    server_socket.close()

def read_user_keys():
    try: 
        #read the keys
        user_private_key = RSA.import_key(open('private.pem').read())
        user_public_key = RSA.import_key(open('public.pem').read())
        print("keys found")
        return user_private_key, user_public_key
    except:
        user_private_key = RSA.generate(2048)
        user_public_key = user_private_key.publickey()
        #save the keys
        user_private_key.export_key()
        user_public_key.export_key()
        #save the keys in private.pem and public.pem
        privatekey_file = open('private.pem', 'wb')
        publickey_file = open('public.pem', 'wb')

        privatekey_file.write(user_private_key.export_key())
        publickey_file.write(user_public_key.export_key())

        print("generated keys", user_private_key, user_public_key)
        return user_private_key, user_public_key

def sign_message(message, user_private_key):
    hash_message = SHA.new(message.encode('utf-8'))
    signature = pkcs1_15.new(user_private_key).sign(hash_message)
    return signature

def validate_signature(user_public_key, hash_message, signature):
    try:
        pkcs1_15.new(user_public_key).verify(hash_message, signature)
        print("Signature is valid")
    except (ValueError, TypeError):
        print("Signature is invalid")

if __name__ == "__main__":
    message = "Amirreza Alasti Sina Mokhtari"
    hash_message = SHA.new(message.encode('utf-8'))
    #convert to hex 
    hash_message_hex = hash_message.hexdigest()

    user_private_key, user_public_key = read_user_keys()

    #sign hash message with private key
    signature = sign_message(message, user_private_key)

    # Assuming you have 'user_public_key', 'hash_message', and 'signature' defined as before
    # validate_signature(user_public_key, hash_message, signature)
    
    final_message = {
        "message": message,
        "signature": signature.hex(),
        "hash_message": hash_message_hex,
    }

    #convert to json
    final_message_json = json.dumps(final_message)
    #convert to bytes
    final_message_bytes = bytes(final_message_json, 'utf-8')

    #encrypt message with aes
    key, cipher, ciphertext, tag, nonce = aes_encryption(final_message_bytes)

    aes_dict_to_encrypt = {
        "key": key.hex(),
        "tag": tag.hex(),
        "nonce": nonce.hex()
    }

    #convert to json
    aes_json = json.dumps(aes_dict_to_encrypt)
    #convert to bytes
    aes_bytes = bytes(aes_json, 'utf-8')
    #encrypting the message with rsa
    private_key, public_key, cipher, encrypted_key = rsa_encryption(aes_bytes)

    #decrypting the key with rsa
    aes_decrypted_json = rsa_decryption(private_key, encrypted_key)

    aes_decrypted_data = json.loads(aes_decrypted_json)

    print(aes_decrypted_data)
    decrypted_key = bytes.fromhex(aes_decrypted_data["key"])
    decrypted_tag = bytes.fromhex(aes_decrypted_data["tag"])
    decrypted_nonce = bytes.fromhex(aes_decrypted_data["nonce"])

    # print(decrypted_key, decrypted_cipher, decrypted_tag, decrypted_nonce)
    # print(decrypted_key == key)
    #decrypting the message with aes
    message_decrypted_json = aes_decryption(decrypted_key, nonce, ciphertext, tag)

    # print(message)

    message_decrypted_data = json.loads(message_decrypted_json)
    print(message_decrypted_data)
    validate_signature(user_public_key, hash_message, signature)






