# 📋 Résumé du Projet Backend - Gestion Scolaire

## 🎯 Vue d'ensemble

Backend Django REST Framework utilisant **MongoDB** pour un système de gestion scolaire complet.

**Technologies** :
- Django 5.2.7
- Django REST Framework 3.16.1
- MongoDB (MongoEngine)
- Authentification par Token personnalisé

---

## 🚀 Commandes de lancement

### 1. Activer l'environnement virtuel

**Windows (PowerShell)** :
```powershell
.\env\Scripts\Activate.ps1
```

**Windows (CMD)** :
```cmd
.\env\Scripts\activate.bat
```

### 2. Lancer le serveur

```bash
python manage.py runserver
```

Le serveur sera accessible sur : `http://127.0.0.1:8000/`

---

## 📡 Endpoints Principaux

### 🔐 Authentification (8 endpoints)
- `POST /api/auth/register/` - Inscription
- `POST /api/auth/login/` - Connexion
- `POST /api/auth/logout/` - Déconnexion
- `GET /api/auth/profile/` - Voir profil
- `PUT /api/auth/profile/` - Modifier profil
- `POST /api/auth/change-password/` - Changer mot de passe
- `GET /api/auth/token-info/` - Infos token
- `POST /api/auth/refresh-token/` - Rafraîchir token

### 👥 CRUD Standard (14 modèles × 5 opérations = 70 endpoints)
Chaque modèle a les opérations GET (liste), GET (détail), POST, PUT/PATCH, DELETE :

1. **Utilisateurs** : `/api/users/`
2. **Élèves** : `/api/eleves/`
3. **Classes** : `/api/classes/`
4. **Matières** : `/api/matieres/`
5. **Devoirs** : `/api/devoirs/`
6. **Années scolaires** : `/api/annees-scolaires/`
7. **Trimestres** : `/api/trimestres/`
8. **Périodes** : `/api/periodes/`
9. **Interrogations** : `/api/interrogations/`
10. **Examens** : `/api/examens/`
11. **Notes trimestrielles** : `/api/notes-trimestrielles/`
12. **Notes annuelles** : `/api/notes-annuelles/`
13. **Messages** : `/api/messages/`
14. **Notifications** : `/api/notifications/`
15. **Emplois du temps** : `/api/emplois-du-temps/`

### ⚙️ Opérations Complexes (5 endpoints)
- `POST /api/calcul-notes-trimestrielles/` - Calcul automatique des notes
- `POST /api/promotion-automatique/` - Promotion automatique des élèves
- `POST /api/affecter-parent/` - Affecter élèves à un parent
- `POST /api/gestion-notifications/` - Marquer toutes notifications lues
- `PATCH /api/marquer-notification-lue/<id>/` - Marquer une notification lue

### 📖 Documentation (3 endpoints)
- `GET /api/schema/` - Schéma OpenAPI
- `GET /api/schema/swagger-ui/` - Interface Swagger
- `GET /api/schema/redoc/` - Documentation ReDoc

**Total : ~86 endpoints**

---

## 🔒 Authentification

Tous les endpoints (sauf register/login) nécessitent un header :
```
Authorization: Token <votre_token>
```

---

## 📊 Rôles Utilisateurs

1. **Développeur** - Accès complet
2. **Administrateur** - Gestion complète
3. **Professeur** - Saisie notes, devoirs, messages
4. **Parent** - Consultation résultats enfants

---

## 📝 Exemple de Requête

### Connexion
```bash
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{
  "email": "jean.dupont@example.com",
  "motDePasse": "motdepasse123"
}
```

### Réponse
```json
{
  "message": "Connexion réussie",
  "user": { ... },
  "token": "abc123..."
}
```

### Utilisation du token
```bash
GET http://localhost:8000/api/eleves/
Authorization: Token abc123...
```

---

## 📚 Documentation Complète

Consultez `DOCUMENTATION_API.md` pour la documentation détaillée avec tous les formats de requêtes/réponses.

---

**Base URL** : `http://localhost:8000`  
**Version** : 1.0.0

