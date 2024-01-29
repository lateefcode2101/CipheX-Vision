import base64
from datetime import time

from gensim.parsing import read_file

from rsaFunctionsForVid import text_to_number, bytes_to_integers, number_to_text, generate_key_pair, encrypt, decrypt
from encryptVideoUsingAESandRSA import *


def first_chunk(action):
    video_file = 'Videos/Original_chunking_Video.mp4'
    public_key_file = 'keys/pubKey/public_key.pem'
    private_key_file = 'keys/privKey/private_key.pem'

    if action == 'encrypt':
        # Encrypt the video file
        encrypted_aes_key, encrypted_video, nonce, tag  = encrypt_video(video_file, public_key_file)
        print("encrypted aes key during encryption is :\n", encrypted_aes_key)

        # Save nonce and tag to a file
        save_tag(tag)
        save_nonce(nonce)

        # Save the encrypted AES key and the encrypted video
        write_file(encrypted_aes_key, 'content/encrypted/encrypted_aes_key.enc')
        write_file(encrypted_video, 'content/encrypted/encrypted_first_video.enc')

    elif action == 'decrypt':
        # Read nonce and tag from file
        nonce = read_nonce()
        tag = read_tag()

        # Decrypt the encrypted AES key and the encrypted video
        encrypted_aes_key = read_file('content/encrypted/encrypted_aes_key.enc')
        encrypted_video = read_file('content/encrypted/encrypted_first_video.enc')
        decrypted_video = decrypt_video(encrypted_aes_key, encrypted_video, nonce, tag, private_key_file)

        # Save the decrypted video
        write_file(decrypted_video, 'content/decrypted/decrypted_first_video.mp4')


def save_nonce(nonce):
    nonce_base64 = base64.b64encode(nonce)
    with open('content/Nonce_Tag_data/nonce.txt', 'w') as file:
        file.write(nonce_base64.decode('utf-8'))

def save_tag(tag):
    tag_base64 = base64.b64encode(tag)
    with open('content/Nonce_Tag_data/tag.txt', 'w') as file:
        file.write(tag_base64.decode('utf-8'))


def read_nonce():
    with open('content/Nonce_Tag_data/nonce.txt', 'r') as file:
        nonce_base64 = file.read()
        nonce = base64.b64decode(nonce_base64)
        print("type of nonce after reading during decryption",type(nonce))
    return nonce

def read_tag():
    with open('content/Nonce_Tag_data/tag.txt', 'r') as file:
        tag_base64 = file.read()
        tag = base64.b64decode(tag_base64)
        print("type of tah after reading during decryption", type(tag))
    return tag
