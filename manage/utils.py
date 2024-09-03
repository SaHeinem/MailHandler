from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

ENCRYPTION_KEY = os.getenv("DJANGO_SECRET").encode()

def encrypt_data(data: str) -> str:
    """
    Encrypts given data with a Fernet cipher.

    :param data: The data to be encrypted.
    :return: The encrypted data as a string.
    """
    fernet = Fernet(ENCRYPTION_KEY)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data: str) -> str:
    """
    Decrypts given encrypted data with a Fernet cipher.

    :param encrypted_data: The data to be decrypted.
    :return: The decrypted data as a string.
    """
    fernet = Fernet(ENCRYPTION_KEY)
    decrypted_data = fernet.decrypt(encrypted_data.encode())
    return decrypted_data.decode()


def set_user_audit_fields(request, obj, change):
    """
    Sets the created_by and modified_by fields of the given object based on the given request and whether or not the object is being created or modified.

    :param request: The request object from which to obtain the user who performed the action
    :param obj: The object being created or modified
    :param change: A boolean indicating whether the object is being created or modified
    """
    if not change or not obj.pk:
        obj.created_by = request.user
    # Always update the user who modified the object
    obj.modified_by = request.user