# Service d'Email Temporaire 📧

Service web permettant de générer et gérer des adresses email temporaires de manière sécurisée.

## 🚀 Fonctionnalités

- ✨ Génération d'emails réalistes avec domaines variés (gmail.com, outlook.fr, etc.)
- 🔄 Expiration automatique des adresses après 24h
- 🎨 Interface moderne avec thème clair/sombre
- 📊 Statistiques en temps réel
- 🔒 Protection contre les abus (rate limiting)
- 📨 Emails de test automatiques

## 📋 Prérequis

- Python 3.12+
- pip (gestionnaire de paquets Python)

## ⚙️ Installation

1. Cloner le projet
```bash
git clone [url-du-projet]
cd "Service d'email temporaire"
```

2. Installer les dépendances
```bash
pip install -r requirements.txt
```

3. Configuration
Créer un fichier `.env` avec :
```env
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_APP=app.py
EMAIL_EXPIRATION_HOURS=24
MAX_TEST_EMAILS=3
LOG_LEVEL=INFO
LOG_FILE=email_service.log
```

## 🚦 Démarrage

1. Lancer l'application
```bash
python app.py
```

2. Accéder à l'interface
Ouvrir http://localhost:5000 dans votre navigateur

## 🔧 Configuration des Domaines

### 👤 Domaines Personnels
Idéal pour les tests et usages personnels :
- gmail.com
- yahoo.fr/com
- hotmail.fr/com
- outlook.fr/com
- laposte.net
- orange.fr
- free.fr
- wanadoo.fr

### 💼 Domaines Professionnels
Pour un usage professionnel et business :
- [votre-entreprise].com
- [votre-entreprise].fr
- [votre-entreprise].net
- [votre-entreprise].org

Pour utiliser un domaine professionnel :
1. Ajoutez votre domaine dans le fichier `.env` :
```env
CUSTOM_DOMAINS=entreprise1.com,entreprise2.fr
```
2. Configurez les enregistrements DNS appropriés
3. Vérifiez la propriété du domaine

### ⚙️ Paramètres par Type de Domaine

#### Domaines Personnels
- Limite : 50 requêtes/IP/heure
- 3 emails de test
- Expiration : 24h

#### Domaines Professionnels
- Limite : 200 requêtes/IP/heure
- 10 emails de test
- Expiration : configurable (1-72h)
- Support prioritaire
- Statistiques détaillées

## 📝 Changelog

### Version 1.0.0 (Date actuelle)
- ✨ Première version stable
- 🎨 Interface utilisateur moderne
- 🔒 Système de rate limiting
- 📧 Génération d'emails réalistes
- 🌓 Support thème clair/sombre

## 🔐 Sécurité

- Rate limiting par IP
- Nettoyage automatique des emails expirés
- Logging des activités
- Protection contre les accès concurrents

## 📚 Structure du Projet

```
Service d'email temporaire/
├── app.py              # Backend Flask
├── requirements.txt    # Dépendances
├── templates/          
│   └── index.html     # Interface utilisateur
├── .env               # Configuration
└── README.md          # Documentation
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.
