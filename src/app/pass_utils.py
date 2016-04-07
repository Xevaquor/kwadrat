import typing
import hashlib
import random
import binascii
import base64

SHA_ITERATIONS = 10 ** 6


def generate_salt() -> str:
    salt = random.SystemRandom().getrandbits(8 * 64)
    binary_salt = int.to_bytes(salt, 64, 'little')
    return base64.encodebytes(binary_salt).decode('utf8', errors='strict')


def hash_password(plain_password: str, salt: str) -> typing.Tuple[str, str]:
    binary_string = bytes(plain_password, encoding='utf8', errors='strict')
    binary_salt = base64.decodebytes(salt.encode('utf8', errors='strict'))

    dk = hashlib.pbkdf2_hmac('sha256', binary_string, binary_salt, SHA_ITERATIONS)

    hash_base64 = base64.encodebytes(dk)

    return hash_base64.decode('utf8', errors='strict')

s = generate_salt()
print(s)
hashed_password = hash_password('Jarosław Polskę zbaw!', s)
print(hashed_password)

hashed2 = hash_password('Jarosław Polskę zbaw!',
                        'iZF2Jqpxrq3jvfbLWYcfVrfTGLpK/9n7FMLQFKM0aeMxNiHBoqGE5eD/VhMMCEpalXQelfcDPUa/LaQlwkxuTA==')

print(hashed2)


