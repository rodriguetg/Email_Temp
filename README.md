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
git clone https://github.com/rodriguetg/service-email-temporaire.git
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

## 👨‍💻 Utilisation

1. Après avoir lancé l'application, accédez à http://localhost:5000
2. Sur l'interface, vous pouvez :
   - Générer une nouvelle adresse email temporaire
   - Voir les emails reçus en temps réel
   - Copier l'adresse générée en un clic
   - Changer le thème (clair/sombre)
   - Voir le temps restant avant expiration

3. Pour les tests :
   - Utilisez le bouton "Envoyer un email test" pour vérifier la réception
   - Les emails de test apparaîtront instantanément dans votre boîte
   - Maximum 3 emails de test par adresse

4. En cas de non réception d'emails :
   - Vérifiez que le serveur est bien lancé
   - Assurez-vous que l'adresse n'a pas expiré
   - Consultez les logs dans `email_service.log`
   - Vérifiez votre connexion internet

## 🔍 Dépannage

Si vous ne recevez pas les codes ou emails :
1. Vérifiez le fichier de log `email_service.log`
2. Assurez-vous que le pare-feu n'empêche pas les connexions
3. Vérifiez que le port 5000 n'est pas utilisé par une autre application
4. Redémarrez le serveur en cas de doute

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

### Version 1.1.0 (Date actuelle)
- ✨ Amélioration de l'interface utilisateur
  - Ajout du curseur pointer pour les notifications cliquables
  - Meilleure interaction visuelle avec les emails
  - Transition fluide pour les éléments interactifs
- 🔄 Optimisation des performances
  - Amélioration de la gestion des événements
  - Meilleure réactivité des notifications

### Version 1.0.0
- ✨ Première version stable
- 🎨 Interface utilisateur moderne
- 🔒 Système de rate limiting
- 📧 Génération d'emails réalistes
- 🌓 Support thème clair/sombre

## 🔜 Prochaines étapes
- [ ] Amélioration de la gestion des pièces jointes
- [ ] Ajout de filtres pour les emails
- [ ] Support pour plus de domaines email
- [ ] Interface d'administration

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

## 📞 Contact & Support

- GitHub: [@rodriguetg](https://github.com/rodriguetg)
- Pour signaler un bug : Ouvrez une issue sur GitHub
- Pour contribuer : Créez une pull request

## 📄 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.
