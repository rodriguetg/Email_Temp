import secrets

# Génère une clé secrète sécurisée de 32 bytes
secret_key = secrets.token_hex(32)
print(f"Votre nouvelle clé secrète est :\n{secret_key}\n")
print("Copiez cette clé et mettez-la dans votre fichier .env comme ceci :")
print(f"SECRET_KEY={secret_key}")
