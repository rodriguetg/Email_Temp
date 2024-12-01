import secrets
import base64

# Génère une clé de 32 bytes (256 bits)
encryption_key = secrets.token_bytes(32)
# Encode en base64 pour une représentation lisible
encryption_key_b64 = base64.b64encode(encryption_key).decode('utf-8')

print(f"Votre nouvelle clé de chiffrement : {encryption_key_b64}")
