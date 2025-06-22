# This module is used by Pinky to handle anything related to AES, which is used to protect its token
# Encryption is only used once to generate an encrypted Discord bot token stored in a .txt file
# Decryption is used upon each instance of running the application in order to access the token via a password
# This system allows Pinky to run using its designated bot token without the token being stored in plaintext anywhere
# If this codebase were to be used with a new bot application, a new token from Discord would need to be encrypted

# NOTE: getpass is notorious for not working when running program in an IDE; if this happens, run directly in
# CLI instead

# Cryptography tools:
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# Used to mask password input when user is prompted for it:
from getpass import getpass
# Base-64 encoding and decoding used in file handling:
from base64 import b64encode, b64decode

# Randomly generated salt and IV are used to marginally enhance resistance to dictionary-type attacks (storing these in
# plaintext does not pose any risk)
SALT = b'\x1c\xae#\x89o\xef\x14,4B\x92T\xe4b\xc8\xfe'
IV = b'\x03M\xbc+\x89{\xce\x1d\\I\xe3ND\xa8\xac\x9e'


# Generate encryption key using password; this password never enters permanent storage and is only used at runtime
def passwordToKey(password: str):
    passBytes = password.encode("utf-8")  # Password must be in byte form to be used with certain function

    # Create a 256-bit AES key derived from the user's password, either for encryption or decryption
    kdf = PBKDF2HMAC(  # Password-Based Key Derivation Function 2 with HMAC (Crazy use of an acronym imo, but okay)
        algorithm=hashes.SHA256(),  # Hashing algorithm: SHA-256 (separate from the AES algorithm that is also used)
        length=32,  # 32 bytes, 256 bits
        salt=SALT,  # Added to make certain password-cracking techniques less effective
        iterations=100000  # More iterations makes the hash stronger, but impacts performance; 100,000 is recommended
    )

    key = kdf.derive(passBytes)  # Note: kdf is short for key-derivation function
    return key


# Encrypt token with AES-256 using key and salt
def encryptToken(key: bytes, token: str):
    cipher = Cipher(algorithms.AES(key), modes.CFB(IV))  # Use AES with 256-bit key and IV
    encryptor = cipher.encryptor()
    # encryptedToken = encryptor.update(b64encode(token)) + encryptor.finalize()  # Encrypt with key
    token_bytes = token.encode("utf-8")
    b64_token = b64encode(token_bytes)
    encryptedToken = encryptor.update(b64_token) + encryptor.finalize()
    return encryptedToken


# Decrypt token using key and salt
def decryptToken(key: bytes, encryptedToken: bytes):
    cipher = Cipher(algorithms.AES(key), modes.CFB(IV))  # Use AES with 256-bit key and IV
    decryptor = cipher.decryptor()
    token = decryptor.update(encryptedToken) + decryptor.finalize()  # Decrypt with key
    return b64decode(token)


# Save token to given filepath
def saveToken(filepath: str, encryptedToken: bytes):
    with open(filepath, "w") as file:  # Encrypted token is encoded in base-64 for storage
        file.write(b64encode(encryptedToken).decode("utf-8"))


# Retrieve token from given filepath
def getToken(filepath: str, key: bytes):
    try:
        with open(filepath, "r") as file:  # Read in file contents
            encryptedToken = b64decode(file.read())
            token = decryptToken(key, encryptedToken)  # Decrypt and return file contents
            return token.decode("utf-8")
    except FileNotFoundError:  # Give error if file not found or unable to be accessed
        print("Error: file could not be accessed. Check that filepath is correct.")


# If script is run directly, prompt user for password and token string for encryption
if __name__ == "__main__":

    token = getpass("Copy and paste your Discord bot token: ")  # Acquire bot token

    password = str
    gettingPassword = True
    while gettingPassword:  # Loop ensures user's password is what they intend it to be by having them enter it twice
        password = getpass("Enter your password (you will be able to verify it was input correctly after): ")
        passCheck = getpass("Enter your password again to ensure it is correct: ")
        if password == passCheck:
            print("Successfully verified password was entered correctly.")
            gettingPassword = False
        else:
            print("Your entries did not match, please try again.")

    filepath = input(  # Get filepath where encrypted token will be stored
        "Enter the filepath to use (do not include extension, file will save as [your filename].txt): "
    ) + ".txt"

    saveToken(filepath, encryptToken(passwordToKey(password), token))  # Encrypt token and save to designated filepath
    print(filepath + ".txt saved successfully!")
