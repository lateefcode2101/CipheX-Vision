from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import math

# Generate ECC key pair
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
public_key = private_key.public_key()
print("private key: ", str(private_key))
print("private key: ", public_key)

# Custom ECC Equation Constants
a = 0  # Coefficient 'a' in the equation y^2 = x^3 + a*x + b
b = 7  # Coefficient 'b' in the equation y^2 = x^3 + a*x + b


def ecc_generate_key(shared_secret):
    # Compute the x coordinate from the shared secret
    x = int.from_bytes(shared_secret, 'big')
    print("x = ", x)

    # Compute the RHS of the ECC equation
    rhs = x ** 3 + a * x + b
    print("rhs = ", rhs)

    # Compute the square root of the RHS
    y = int(math.sqrt(rhs))

    return y


# Perform ECDH key exchange to obtain the shared secret
shared_secret = private_key.exchange(ec.ECDH(), public_key)

# Generate ECC-based key using the shared secret
ecc_key = ecc_generate_key(shared_secret)

print("ECC Key:", ecc_key)
