import base64
from dotenv import dotenv_values
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken, InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC  # (Password-Based Key Derivation Function 2)


class CryptoFile:
    def __init__(self, file, new_file, mode, password):
        self.file = file
        self.mode = mode
        self.new_file = new_file
        self.password = password
        # self.new_path = new_path
        self.handler = None
        self.new_handler = None

    def __enter__(self):
        self.handler = open(self.file)

        config = dotenv_values('.env')
        self.salt = config['SALT'].encode('UTF-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=960000
        )
        self.key = base64.urlsafe_b64encode(kdf.derive(self.password.encode('UTF-8')))

        return self

    def encrypt_mode(self):
        self.new_handler = open(file=self.new_file, mode='wb')
        decrypted_content = self.handler.read()

        fernet = Fernet(self.key)
        token = fernet.encrypt(data=decrypted_content.encode('UTF-8'))

        self.new_handler.write(token)

    def decrypt_mode(self):
        self.new_handler = open(file=self.new_file, mode='w')

        token = self.handler.read()
        fernet = Fernet(self.key)

        try:
            decrypted_content = fernet.decrypt(token=token)
            self.new_handler.write(decrypted_content.decode('UTF-8'))
        except(InvalidToken, InvalidSignature):
            print("Something went wrong")

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.handler.close()
        self.new_handler.close()
