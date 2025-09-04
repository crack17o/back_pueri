# Système de Gestion Scolaire - Django + MongoDB

## 📋 Description
Système complet de gestion scolaire développé avec Django et MongoDB, permettant la gestion des utilisateurs, élèves, classes, matières, notes, emplois du temps, communications et notifications.

## 🚀 Fonctionnalités Principales

### 👥 Gestion des Utilisateurs
- **4 rôles** : Développeur, Administrateur, Professeur, Parent
- **Permissions granulaires** selon le rôle
- **Authentification** et autorisation API

### 🎓 Gestion des Élèves
- **Inscription** et **affectation automatique/manuelle** aux subdivisions
- **Lien** avec les parents
- **Historique complet** des parcours

### 📚 Classes et Subdivisions
- **Primaire** (1-6) : subdivisions avec professeur principal
- **Secondaire** (7-8) : professeurs par matière
- **Affectation aléatoire ou manuelle** des subdivisions

### 📝 Saisie et Calcul des Notes
- **Travaux/Interrogations** → 50% de la note trimestrielle
- **Examens** → 50% de la note trimestrielle
- **Note annuelle** : moyenne des 3 trimestres
- **Promotion automatique** basée sur le seuil

### 📅 Gestion du Temps
- **Années scolaires**, **trimestres** et **périodes**
- **Emplois du temps fixes** pour toute l'année
- **Cours "Pause"** pour marquer les pauses

### 💬 Communication
- **Messages** entre parents et professeurs
- **Notifications** pour devoirs et messages
- **Filtrage** par type et statut (lu/non lu)

## 🛠️ Technologies Utilisées

- **Backend** : Django 5.2.6
- **Base de données** : MongoDB (avec mongoengine)
- **API** : Django REST Framework
- **Authentification** : Token-based authentication
- **Permissions** : Système de rôles personnalisé

## 📦 Installation

### Prérequis
- Python 3.8+
- MongoDB 4.4+
- pip et virtualenv

### Configuration

1. **Remplir le fichier `.env`** avec vos informations MongoDB :
```env
MONGODB_HOST=mongodb+srv://your-cluster.mongodb.net
MONGODB_DB_NAME=gestion_scolaire_db
MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password
DEBUG=True
SECRET_KEY=your-secret-key-here
```

2. **Activer l'environnement virtuel** :
```bash
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Lancer le serveur de développement** :
```bash
python manage.py runserver
```

4. **Initialiser les données de test** :
```bash
python init_data.py
```

5. **Lancer les tests** :
```bash
python manage.py test
```

## 📡 API Endpoints

### Base URL : `http://localhost:8000/api/`

#### 🔐 Authentification
| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/auth/register/` | POST | Inscription d'un nouvel utilisateur |
| `/auth/login/` | POST | Connexion utilisateur |
| `/auth/logout/` | POST | Déconnexion utilisateur |
| `/auth/profile/` | GET/PUT | Consultation/modification du profil |
| `/auth/change-password/` | POST | Changement de mot de passe |

#### 📚 Gestion des Données
| Endpoint | Description |
|----------|-------------|
| `/users/` | Gestion des utilisateurs |
| `/eleves/` | Gestion des élèves |
| `/classes/` | Gestion des classes |
| `/matieres/` | Gestion des matières |
| `/devoirs/` | Gestion des devoirs |
| `/annees-scolaires/` | Gestion des années scolaires |
| `/trimestres/` | Gestion des trimestres |
| `/periodes/` | Gestion des périodes |
| `/interrogations/` | Gestion des interrogations |
| `/examens/` | Gestion des examens |
| `/notes-trimestrielles/` | Notes trimestrielles |
| `/notes-annuelles/` | Notes annuelles |
| `/messages/` | Messagerie |
| `/notifications/` | Notifications |
| `/emplois-du-temps/` | Emplois du temps |

### Actions Spéciales ✨

- **POST** `/eleves/affecter_subdivision_auto/` - Affectation automatique des subdivisions
- **POST** `/notes-trimestrielles/calculer_notes_trimestrielles/` - Calcul automatique des notes
- **POST** `/notes-annuelles/promotion_automatique/` - Promotion automatique des élèves
- **PATCH** `/notifications/{id}/marquer_lu/` - Marquer notification comme lue
- **POST** `/notifications/marquer_toutes_lues/` - Marquer toutes les notifications comme lues

## 🔐 Exemples d'Utilisation de l'API

### Inscription d'un nouvel utilisateur
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Dupont",
    "prenom": "Jean",
    "email": "jean.dupont@example.com",
    "motDePasse": "motdepasse123",
    "role": "parent",
    "telephone": "0123456789"
  }'
```

### Connexion
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jean.dupont@example.com",
    "motDePasse": "motdepasse123"
  }'
```

### Consultation du profil (avec token)
```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Token your-token-here"
```

### Calcul automatique des notes trimestrielles
```bash
curl -X POST http://localhost:8000/api/notes-trimestrielles/calculer_notes_trimestrielles/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{"trimestre_id": "trimestre_id_here"}'
```

## 🔐 Autorisations par Rôle

### Développeur 🔧
- **CRUD complet** sur toutes les entités
- **Accès** à toutes les données
- **Gestion** des utilisateurs et rôles

### Administrateur 👨‍💼
- **Gestion complète** de toutes les entités
- **Configuration** des emplois du temps et années scolaires
- **Répartition manuelle** des subdivisions
- **Consultation** de toutes les notes et messages

### Professeur 👨‍🏫
- **Saisie/modification** des notes pendant les périodes actives
- **Consultation** des résultats de sa subdivision
- **Envoi/réception** de messages avec notifications
- **Création** de devoirs

### Parent 👨‍👩‍👧‍👦
- **Consultation** des résultats de ses enfants
- **Consultation** des emplois du temps
- **Réception** de notifications et messages
- **Communication** avec les professeurs

## 🗃️ Structure des Modèles

### Collections MongoDB

1. **User** - Utilisateurs du système
2. **Eleve** - Données des élèves
3. **Classe** - Classes avec subdivisions
4. **Matiere** - Matières et coefficients
5. **Devoir** - Devoirs assignés
6. **AnneeScolaire** - Configuration annuelle
7. **Trimestre** - Périodes trimestrielles
8. **Periode** - Périodes de saisie
9. **Interrogation** - Notes de travaux
10. **Examen** - Notes d'examens
11. **NoteTrimestrielle** - Notes calculées par trimestre
12. **NoteAnnuelle** - Notes annuelles et promotions
13. **Message** - Communication inter-utilisateurs
14. **Notification** - Système de notifications
15. **EmploiDuTemps** - Planification des cours

## 🎯 Logique Métier

### Calcul des Notes
```python
# Note trimestrielle = (Moyenne Travaux * 0.5) + (Note Examen * 0.5)
# Note annuelle = (Trimestre1 + Trimestre2 + Trimestre3) / 3
```

### Promotion Automatique
- Basée sur le **seuil de promotion** de chaque classe
- **Répartition aléatoire** ou **choix manuel** des nouvelles subdivisions
- **Historique** conservé pour toutes les années

### Notifications Automatiques
- **Nouveau devoir** → Notification aux parents des élèves concernés
- **Nouveau message** → Notification au destinataire
- **Filtrage** par type et statut de lecture

## 📁 Structure du Projet

```
gestion_scolaire/
├── core/
│   ├── models.py          # Modèles MongoDB
│   ├── serializers.py     # Serializers API
│   ├── views.py          # ViewSets API
│   ├── permissions.py    # Permissions par rôle
│   ├── services.py       # Logique métier
│   └── urls.py          # Routes API
├── gestion_scolaire/
│   ├── settings.py      # Configuration Django
│   └── urls.py         # URLs principales
└── manage.py           # Script Django
```

## 🚀 Démarrage Rapide

1. **Créer un superutilisateur développeur** :
```python
from core.models import User
dev_user = User(
    nom="Admin",
    prenom="System", 
    email="admin@school.com",
    motDePasse="admin123",
    role="developpeur"
)
dev_user.save()
```

2. **Tester l'API** :
```bash
curl -X GET http://localhost:8000/api/users/
```

## 📈 Évolutions Futures

- [ ] Interface Web avec React/Vue.js
- [ ] Authentification OAuth2
- [ ] Système de rapports et statistiques
- [ ] Notifications push mobiles
- [ ] Intégration avec systèmes externes
- [ ] Module de comptabilité/finances

## 📞 Support

Pour toute question ou problème, veuillez consulter la documentation ou créer une issue dans le repository.

---
**Version** : 1.0.0  
**Dernière mise à jour** : Septembre 2025
