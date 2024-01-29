from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


# Function to generate a random AES key
def generate_aes_key():
    with open('keys/aesKey/aes_key.txt', 'rb') as file:
        aes_key = file.read().strip()
        print("type of aes key read is ",type(aes_key))
    return aes_key  # AES key size is 16 bytes (128 bits)


# Function to read the video file
def read_video_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()


# Function to write data to a file
def write_file(data, file_path):
    with open(file_path, 'wb') as f:
        f.write(data)


# Function to encrypt data using AES
def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext, cipher.nonce, tag


# Function to decrypt data using AES
def aes_decrypt(ciphertext, key, nonce, tag):
    nonce_bytes = nonce #.encode('utf-8') if isinstance(nonce, str) else nonce # Convert nonce string to bytes using UTF-8 encoding
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce_bytes)
    tag_bytes = tag #.encode('utf-8') if isinstance(tag, str) else tag
    plaintext = cipher.decrypt_and_verify(ciphertext, tag_bytes)
    return plaintext


# Function to encrypt the video file using RSA for the AES key
def encrypt_video(video_file, public_key_file):
    # Read the video file
    video_data = read_video_file(video_file)

    # Generate a random AES key
    aes_key = generate_aes_key()

    # Encrypt the video data using AES
    encrypted_video, nonce, tag = aes_encrypt(video_data, aes_key)
    print("type of nonce during encryption is ",type(nonce))
    print("type of tag during encryption is ", type(tag))

    # Read the public key
    with open(public_key_file, 'rb') as f:
        public_key = RSA.import_key(f.read())

    # Initialize the cipher with the public key
    cipher_rsa = PKCS1_OAEP.new(public_key)

    # Encrypt the AES key using RSA
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    print("len(encrypted_aes_key) = ",len(encrypted_aes_key))
    print(encrypted_aes_key)

    return encrypted_aes_key, encrypted_video, nonce, tag


# Function to decrypt the video file using RSA for the AES key
def decrypt_video(encrypted_aes_key, encrypted_video, nonce, tag, private_key_file):
    # Read the private key
    with open(private_key_file, 'rb') as f:
        private_key = RSA.import_key(f.read())
    print(len(encrypted_aes_key))
    # Initialize the cipher with the private key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    print("encrypted aes key during decryption is : ", encrypted_aes_key)

    # Decrypt the AES key using RSA
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    print("lenght of aesk key" ,len(aes_key))

    # Decrypt the video data using AES
    decrypted_video = aes_decrypt(encrypted_video, aes_key, nonce, tag)

    return decrypted_video


# # Example usage
# video_file = 'sampleTests/word2vec Tests/Original_chunking_Video.mp4'
# public_key_file = 'sampleTests/word2vec Tests/public_key.pem'
# private_key_file = 'sampleTests/word2vec Tests/private_key.pem'
#
# # Encrypt the video file
# encrypted_aes_key, encrypted_video, nonce, tag = encrypt_video(video_file, public_key_file)
#
# # Save the encrypted AES key and the encrypted video
# write_file(encrypted_aes_key, 'sampleTests/word2vec Tests/encrypted_aes_key.enc')
# write_file(encrypted_video, 'sampleTests/word2vec Tests/encrypted_video.enc')
#
# # Decrypt the encrypted AES key and the encrypted video
# encrypted_aes_key = read_video_file('sampleTests/word2vec Tests/encrypted_aes_key.enc')
# encrypted_video = read_video_file('sampleTests/word2vec Tests/encrypted_video.enc')
# decrypted_video = decrypt_video(encrypted_aes_key, encrypted_video, nonce, tag, private_key_file)
#
# # Save the decrypted video
# write_file(decrypted_video, 'sampleTests/word2vec Tests/decrypted_video.mp4')
