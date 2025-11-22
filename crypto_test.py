# crypto.py
"""
import random
from sympy import isprime
from math import gcd

def gen_prime(bits=16):
    # Génère un nombre premier de 'bits' bits (petit pour tests)
    while True:
        p = random.getrandbits(bits) | 1
        if isprime(p):
            return p

def egcd(a, b):
    if b == 0:
        return (1, 0, a)
    x, y, g = egcd(b, a % b)
    return (y, x - (a // b) * y, g)

def modinv(a, m):
    x, y, g = egcd(a, m)
    if g != 1:
        raise Exception("modinv does not exist")
    return x % m

def generate_keypair(bits=32):
    # Retourne (pub_n, pub_e), (priv_n, priv_d)
    p = gen_prime(bits//2)
    q = gen_prime(bits//2)
    while q == p:
        q = gen_prime(bits//2)
    n = p * q
    phi = (p - 1) * (q - 1)
    # choose e coprime with phi
    e = 65537
    if gcd(e, phi) != 1:
        # fallback
        e = 3
        while gcd(e, phi) != 1:
            e += 2
    d = modinv(e, phi)
    return (n, e), (n, d)

def encrypt_int(m_int, pub):
    n, e = pub
    return pow(m_int, e, n)

def decrypt_int(c_int, priv):
    n, d = priv
    return pow(c_int, d, n)

# helpers to convert bytes <-> int
def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder='big')

def int_to_bytes(i: int) -> bytes:
    blen = (i.bit_length() + 7) // 8
    return i.to_bytes(blen, byteorder='big')
"""