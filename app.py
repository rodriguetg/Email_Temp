import os
import json
import time
import random
import string
import hashlib
import logging
import threading
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, render_template
from functools import wraps

# Configuration du logging
logging.basicConfig(
    filename='email_service.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Noms français pour la génération d'emails
PRENOMS = ['Jean', 'Pierre', 'Marie', 'Sophie', 'Lucas', 'Emma', 'Louis', 'Léa', 'Thomas', 'Camille',
           'Nicolas', 'Antoine', 'Julie', 'Sarah', 'Paul', 'Claire', 'Marc', 'Laura', 'David', 'Anne']

NOMS = ['Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit', 'Durand', 'Leroy', 'Moreau',
        'Laurent', 'Simon', 'Michel', 'Garcia', 'David', 'Bertrand', 'Roux', 'Vincent', 'Fournier', 'Morel']

# Configuration des domaines
PERSONAL_DOMAINS = [
    'outlook.fr',
    'outlook.com',
    'gmail.com',
    'yahoo.fr',
    'yahoo.com',
    'laposte.net',
    'orange.fr',
    'free.fr',
    'wanadoo.fr',
    'hotmail.fr',
    'hotmail.com'
]

# Charger les domaines professionnels depuis .env
PROFESSIONAL_DOMAINS = os.getenv('CUSTOM_DOMAINS', '').split(',') if os.getenv('CUSTOM_DOMAINS') else []

def is_professional_domain(domain):
    return domain in PROFESSIONAL_DOMAINS

def get_rate_limit(domain):
    if is_professional_domain(domain):
        return 200  # 200 requêtes/heure pour les domaines pro
    return 50      # 50 requêtes/heure pour les domaines personnels

def get_expiration_hours(domain):
    if is_professional_domain(domain):
        return int(os.getenv('PRO_EMAIL_EXPIRATION_HOURS', '168'))  # 7 jours par défaut pour les pros
    return int(os.getenv('EMAIL_EXPIRATION_HOURS', '72'))  # 3 jours par défaut pour les persos

def get_max_test_emails(domain):
    if is_professional_domain(domain):
        return 10  # 10 emails de test pour les domaines pro
    return 3      # 3 emails de test pour les domaines personnels

class EmailStorage:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(EmailStorage, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.emails = {}
        self.stats = {'active_addresses': 0, 'total_messages': 0}
        self._start_cleanup_thread()

    def _start_cleanup_thread(self):
        def cleanup_expired():
            while True:
                try:
                    current_time = time.time()
                    with self._lock:
                        expired = [email for email, data in self.emails.items() 
                                if data['expiration'] < current_time]
                        
                        for email in expired:
                            logging.info(f"Suppression de l'adresse expirée: {email}")
                            del self.emails[email]
                            self.stats['active_addresses'] = max(0, self.stats['active_addresses'] - 1)
                except Exception as e:
                    logging.error(f"Erreur dans le thread de nettoyage: {str(e)}")
                finally:
                    time.sleep(60)

        thread = threading.Thread(target=cleanup_expired, daemon=True)
        thread.start()

    def generate_email(self):
        with self._lock:
            prenom = random.choice(PRENOMS).lower()
            nom = random.choice(NOMS).lower()
            
            # Sélection du domaine en fonction du type d'utilisation
            if PROFESSIONAL_DOMAINS and random.random() < 0.3:  # 30% de chance d'avoir un domaine pro si disponible
                domain = random.choice(PROFESSIONAL_DOMAINS)
            else:
                domain = random.choice(PERSONAL_DOMAINS)
            
            # Différents formats d'email
            formats = [
                f"{prenom}.{nom}",
                f"{prenom}{nom}",
                f"{prenom[0]}{nom}",
                f"{prenom}.{nom[0]}",
                f"{nom}.{prenom}",
                f"{prenom}_{nom}"
            ]
            
            base = random.choice(formats)
            
            # Ajoute des chiffres de manière plus naturelle
            if random.random() < 0.7:  # 70% de chance d'avoir des chiffres
                if random.random() < 0.5:  # 50% de chance d'avoir une année
                    year = random.randint(1960, 2005)
                    base = f"{base}{year}"
                else:
                    num = random.randint(1, 999)
                    base = f"{base}{num}"
            
            email = f"{base}@{domain}"
            
            expiration = time.time() + get_expiration_hours(domain) * 60 * 60  # expiration en fonction du domaine
            self.emails[email] = {
                'messages': [],
                'expiration': expiration,
                'created_at': time.time()
            }
            
            self.stats['active_addresses'] += 1
            logging.info(f"Nouvelle adresse générée: {email}")
            
            return email, expiration

    def add_test_email(self, to_email):
        with self._lock:
            if to_email not in self.emails:
                return False
            
            email_data = self.emails[to_email]
            if email_data['expiration'] < time.time():
                return False

            msg_id = hashlib.sha256(f"{to_email}{time.time()}".encode()).hexdigest()[:12]
            
            # Codes de vérification plus visibles
            verification_codes = [
                "123456",
                "789012",
                "345678"
            ]
            
            subjects = [
                "Code de vérification",
                "Votre code d'accès",
                "Code de sécurité"
            ]
            
            bodies = [
                f"Votre code de vérification est : {verification_codes[0]}",
                f"Utilisez ce code d'accès : {verification_codes[1]}",
                f"Code de sécurité temporaire : {verification_codes[2]}"
            ]
            
            attachments = [
                [],
                ["document.pdf", "image.jpg"],
                ["verification.pdf"]
            ]
            
            idx = len(email_data['messages']) % 3
            
            message = {
                'id': msg_id,
                'from': 'service@temp-mail.fr',
                'subject': subjects[idx],
                'body': bodies[idx],
                'date': datetime.now().isoformat(),
                'read': False,
                'attachments': attachments[idx]
            }
            
            email_data['messages'].append(message)
            self.stats['total_messages'] += 1
            
            logging.info(f"Email de test ajouté pour: {to_email}")
            return True

    def get_messages(self, email):
        with self._lock:
            if email not in self.emails:
                return None
            
            email_data = self.emails[email]
            if email_data['expiration'] < time.time():
                return None
            
            return {
                'emails': email_data['messages'],
                'expiration': email_data['expiration']
            }

    def mark_as_read(self, email, message_id):
        with self._lock:
            if email not in self.emails:
                return False
            
            email_data = self.emails[email]
            if email_data['expiration'] < time.time():
                return False
            
            for message in email_data['messages']:
                if message['id'] == message_id:
                    message['read'] = True
                    logging.info(f"Message {message_id} marqué comme lu pour {email}")
                    return True
            
            return False

    def get_stats(self):
        with self._lock:
            return self.stats.copy()

# Rate limiting simple
def rate_limit(f):
    requests = {}
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = request.remote_addr
        current_time = time.time()
        
        # Nettoie les anciennes entrées
        requests.clear()  # Simplifié pour éviter les problèmes de thread
        
        if ip not in requests:
            requests[ip] = []
        
        requests[ip].append(current_time)
        
        # Limite simple : 50 requêtes par IP
        if len(requests[ip]) > get_rate_limit(request.remote_addr):
            return jsonify({'error': 'Trop de requêtes'}), 429
        
        return f(*args, **kwargs)
    
    return decorated_function

# Instance globale du stockage d'emails
email_storage = EmailStorage()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
@rate_limit
def generate_email():
    try:
        email, expiration = email_storage.generate_email()
        
        def add_test_emails():
            try:
                for _ in range(get_max_test_emails(email.split('@')[1])):
                    if email_storage.add_test_email(email):
                        time.sleep(random.uniform(5, 15))
            except Exception as e:
                logging.error(f"Erreur lors de l'ajout d'emails de test: {str(e)}")
        
        threading.Thread(target=add_test_emails, daemon=True).start()
        
        return jsonify({
            'email': email,
            'expiration': expiration * 1000
        })
    except Exception as e:
        logging.error(f"Erreur lors de la génération d'email: {str(e)}")
        return jsonify({'error': 'Erreur lors de la génération de l\'email'}), 500

@app.route('/check/<email>')
@rate_limit
def check_email(email):
    try:
        messages = email_storage.get_messages(email)
        if messages is None:
            return jsonify({'error': 'Email non trouvé ou expiré'}), 404
        return jsonify(messages)
    except Exception as e:
        logging.error(f"Erreur lors de la vérification des emails: {str(e)}")
        return jsonify({'error': 'Erreur lors de la vérification des emails'}), 500

@app.route('/mark_read/<email>/<message_id>')
@rate_limit
def mark_read(email, message_id):
    try:
        if email_storage.mark_as_read(email, message_id):
            return jsonify({'success': True})
        return jsonify({'error': 'Message non trouvé'}), 404
    except Exception as e:
        logging.error(f"Erreur lors du marquage comme lu: {str(e)}")
        return jsonify({'error': 'Erreur lors du marquage comme lu'}), 500

@app.route('/stats')
def get_stats():
    try:
        return jsonify(email_storage.get_stats())
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des stats: {str(e)}")
        return jsonify({'error': 'Erreur lors de la récupération des stats'}), 500

if __name__ == '__main__':
    print(" * Accédez à l'application à l'adresse : http://localhost:5000")
    app.run(debug=True, host='0.0.0.0')
