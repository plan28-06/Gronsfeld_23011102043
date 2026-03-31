MOD = 2**16


# Convert input to uppercase and retain only A–Z characters.
def normalize_text(text: str) -> str:
    return ''.join(c for c in text.upper() if 'A' <= c <= 'Z')


# Encrypt plaintext using the Gronsfeld cipher with a cyclic numeric key.
def encrypt_gronsfeld(plaintext: str, key: str) -> str:
    key_len = len(key)
    return ''.join(
        chr(((ord(char) - ord('A') + int(key[i % key_len])) % 26) + ord('A'))
        for i, char in enumerate(plaintext)
    )


# Compute 16-bit hash: sum of ASCII values modulo 2^16, returned as 4-digit hex.
def compute_hash(ciphertext: str) -> str:
    return format(sum(ord(c) for c in ciphertext) % MOD, '04x')


# Concatenate ciphertext and hash to form the final message.
def create_message(ciphertext: str, hash_val: str) -> str:
    return f"{ciphertext}{hash_val}"


# Validate message integrity by recomputing and comparing the hash.
def verify_message(message: str):
    ciphertext, received_hash = message[:-4], message[-4:]
    return compute_hash(ciphertext) == received_hash, ciphertext


# Decrypt ciphertext using the Gronsfeld cipher with the same cyclic key.
def decrypt_gronsfeld(ciphertext: str, key: str) -> str:
    key_len = len(key)
    return ''.join(
        chr(((ord(char) - ord('A') - int(key[i % key_len]) + 26) % 26) + ord('A'))
        for i, char in enumerate(ciphertext)
    )


# End-to-end sender pipeline: normalize, encrypt, hash, and package message.
def sender(plaintext: str, key: str) -> str:
    normalized = normalize_text(plaintext)
    ciphertext = encrypt_gronsfeld(normalized, key)
    return create_message(ciphertext, compute_hash(ciphertext))


# End-to-end receiver pipeline: verify integrity and decrypt if valid.
def receiver(message: str, key: str) -> str:
    is_valid, ciphertext = verify_message(message)
    if not is_valid:
        return "Message is corrupted or tampered!"
    return decrypt_gronsfeld(ciphertext, key)


if __name__ == "__main__":
    key = "31415"
    plaintext = "HELLO WORLD"

    message = sender(plaintext, key)
    result = receiver(message, key)

    print("Transmitted Message:", message)
    print("Decrypted Plaintext:", result)