# What is RSA
RSA is an asymmetric encryption algorithm that uses a public key and a private key to encrypt and decrypt messages. It’s one of the most secure encryption methods after AES, and it’s used in most modern applications including web browsers and secure email services.

## Symmetric Vs Asymmetric Encryption
AES is a <b> symmetric-key algorithm </b>, meaning the same key (aka passphrase or password) is used to encrypt and decrypt the data. This characteristic presents pros and cons detailed in the following sections.

Asymmetric methods use a public key for encryption and a secret key for decryption. Anyone can send encrypted messages but only the receiver knows how to decrypt them. TLS certificates used for secure HTTP communication (HTTPS) leverage asymmetric encryption, for example.

## How RSA Works
RSA is based on the difficulty of factoring large integers. The public key is a pair of numbers (e, n) where e is the exponent and n is the modulus. The private key is a pair of numbers (d, n) where d is the exponent and n is the same modulus as before.

The modulus n is the product of two large prime numbers p and q. The public key exponent e is a number between 1 and n that is coprime to (p-1)(q-1). The private key exponent d is the multiplicative inverse of e modulo (p-1)(q-1).


## Encryption

To encrypt a message m, the sender computes c = m^e mod n and sends the ciphertext c to the receiver. The receiver decrypts the ciphertext using the private key exponent d: m = c^d mod n.

## Key Generation

The first step in RSA is to generate the public and private keys. The following code snippet shows how to generate a key pair using the RSA module in Python.

```python
from Crypto.PublicKey import RSA

key = RSA.generate(2048)
private_key = key.export_key()
file_out = open("private.pem", "wb")
file_out.write(private_key)

public_key = key.publickey().export_key()
file_out = open("receiver.pem", "wb")
file_out.write(public_key)
```

The code above generates a 2048-bit RSA key pair, saves the private key in a file named private.pem and the public key in a file named receiver.pem.

## pros and cons of RSA

### Pros
- RSA is one of the most secure encryption methods after AES.
- It’s an asymmetric algorithm, meaning you can encrypt messages without exchanging a secret key beforehand.
- It’s used in most modern applications including web browsers and secure email services.
- It’s an open standard and there are no known vulnerabilities.
  
### Cons
- It’s slow compared to symmetric algorithms such as AES.
- It can only encrypt messages that are smaller than the key size.
- It’s not suitable for encrypting large amounts of data.
- It’s not suitable for encrypting with low-power devices such as smartphones.

## use cases
- RSA is used in most modern applications including web browsers and secure email services.


## References
- https://en.wikipedia.org/wiki/RSA_(cryptosystem)
- https://www.youtube.com/watch?v=4zahvcJ9glg
