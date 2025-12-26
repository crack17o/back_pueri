# 📚 Documentation API - Système de Gestion Scolaire

## 🎯 Vue d'ensemble

Backend Django REST Framework utilisant **MongoDB** (via MongoEngine) pour la gestion d'un système scolaire complet.

**Base URL** : `http://localhost:8000`

---

## 🚀 Commandes pour lancer le serveur

### 1. Activer l'environnement virtuel (venv)

**Sur Windows (PowerShell)** :
```powershell
.\env\Scripts\Activate.ps1
```

**Sur Windows (CMD)** :
```cmd
.\env\Scripts\activate.bat
```

**Sur Linux/Mac** :
```bash
source env/bin/activate
```

### 2. Installer les dépendances (si nécessaire)

```bash
pip install -r requirements.txt
```

### 3. Lancer le serveur de développement

```bash
python manage.py runserver
```

Le serveur sera accessible sur : `http://127.0.0.1:8000/`

### 4. (Optionnel) Initialiser les données de test

```bash
python init_data.py
```

---

## 🔐 Authentification

L'authentification se fait via **Token** dans le header :
```
Authorization: Token <votre_token>
```

---

## 📡 Liste complète des Endpoints

### 🔑 Authentification

#### 1. **POST** `/api/auth/register/`
Inscription d'un nouvel utilisateur

**Permissions** : Aucune (AllowAny)

**Body (JSON)** :
```json
{
  "nom": "Dupont",
  "prenom": "Jean",
  "email": "jean.dupont@example.com",
  "motDePasse": "motdepasse123",
  "role": "parent",  // "parent" | "professeur" | "admin" | "developpeur"
  "telephone": "0123456789"  // Optionnel
}
```

**Réponse (201 Created)** :
```json
{
  "message": "Utilisateur créé avec succès",
  "user": {
    "id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "nom": "Dupont",
    "prenom": "Jean",
    "email": "jean.dupont@example.com",
    "role": "parent"
  },
  "token": "abc123def456..."
}
```

---

#### 2. **POST** `/api/auth/login/`
Connexion d'un utilisateur

**Permissions** : Aucune (AllowAny)

**Body (JSON)** :
```json
{
  "email": "jean.dupont@example.com",
  "motDePasse": "motdepasse123"
}
```

**Réponse (200 OK)** :
```json
{
  "message": "Connexion réussie",
  "user": {
    "id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "nom": "Dupont",
    "prenom": "Jean",
    "email": "jean.dupont@example.com",
    "role": "parent",
    "telephone": "0123456789"
  },
  "token": "abc123def456..."
}
```

---

#### 3. **POST** `/api/auth/logout/`
Déconnexion d'un utilisateur

**Permissions** : Authentifié

**Headers** :
```
Authorization: Token <votre_token>
```

**Réponse (200 OK)** :
```json
{
  "message": "Déconnexion réussie"
}
```

---

#### 4. **GET** `/api/auth/profile/`
Consultation du profil utilisateur

**Permissions** : Authentifié

**Headers** :
```
Authorization: Token <votre_token>
```

**Réponse (200 OK)** :
```json
{
  "id": "65a1b2c3d4e5f6g7h8i9j0k1",
  "nom": "Dupont",
  "prenom": "Jean",
  "email": "jean.dupont@example.com",
  "role": "parent",
  "telephone": "0123456789",
  "enfants": []
}
```

---

#### 5. **PUT** `/api/auth/profile/`
Modification du profil utilisateur

**Permissions** : Authentifié

**Headers** :
```
Authorization: Token <votre_token>
```

**Body (JSON)** :
```json
{
  "nom": "Martin",
  "prenom": "Pierre",
  "telephone": "0987654321"
}
```

**Réponse (200 OK)** :
```json
{
  "message": "Profil mis à jour avec succès",
  "user": {
    "id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "nom": "Martin",
    "prenom": "Pierre",
    "email": "jean.dupont@example.com",
    "role": "parent",
    "telephone": "0987654321"
  }
}
```

---

#### 6. **POST** `/api/auth/change-password/`
Changement de mot de passe

**Permissions** : Authentifié

**Headers** :
```
Authorization: Token <votre_token>
```

**Body (JSON)** :
```json
{
  "ancien_mot_de_passe": "ancien123",
  "nouveau_mot_de_passe": "nouveau123"
}
```

**Réponse (200 OK)** :
```json
{
  "message": "Mot de passe modifié avec succès"
}
```

---

#### 7. **GET** `/api/auth/token-info/`
Informations sur le token actuel

**Permissions** : Authentifié

**Headers** :
```
Authorization: Bearer <votre_token>
```

**Réponse (200 OK)** :
```json
{
  "token_key": "abc123def4...",
  "created": "2025-01-15T10:30:00Z",
  "user": {
    "id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "email": "jean.dupont@example.com",
    "role": "parent"
  }
}
```

---

#### 8. **POST** `/api/auth/refresh-token/`
Actualiser le token

**Permissions** : Authentifié

**Headers** :
```
Authorization: Bearer <ancien_token>
```

**Réponse (200 OK)** :
```json
{
  "message": "Token actualisé avec succès",
  "token": "nouveau_token_abc123..."
}
```

---

### 👥 Gestion des Utilisateurs

#### 9. **GET** `/api/users/`
Liste tous les utilisateurs

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets User

---

#### 10. **GET** `/api/users/<id>/`
Récupère un utilisateur par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet User

---

#### 11. **POST** `/api/users/`
Crée un nouvel utilisateur

**Permissions** : Authentifié

**Body (JSON)** :
```json
{
  "nom": "Dupont",
  "prenom": "Jean",
  "email": "jean.dupont@example.com",
  "motDePasse": "motdepasse123",
  "role": "parent",
  "telephone": "0123456789"
}
```

**Réponse (201 Created)** : Objet User créé

---

#### 12. **PUT** `/api/users/<id>/`
Met à jour complètement un utilisateur

**Permissions** : Authentifié

**Body (JSON)** : Tous les champs de l'utilisateur

**Réponse (200 OK)** : Objet User mis à jour

---

#### 13. **PATCH** `/api/users/<id>/`
Met à jour partiellement un utilisateur

**Permissions** : Authentifié

**Body (JSON)** : Champs à modifier uniquement

**Réponse (200 OK)** : Objet User mis à jour

---

#### 14. **DELETE** `/api/users/<id>/`
Supprime un utilisateur

**Permissions** : Authentifié

**Réponse (204 No Content)**

---

### 🎓 Gestion des Élèves

#### 15. **GET** `/api/eleves/`
Liste tous les élèves

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets Eleve

---

#### 16. **GET** `/api/eleves/<id>/`
Récupère un élève par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet Eleve avec structure :
```json
{
  "id": "...",
  "nom": "Martin",
  "prenom": "Sophie",
  "matricule": "MAT001",
  "dateNaissance": "2010-05-15T00:00:00Z",
  "classe": "class_id",
  "subdivision": "A",
  "parents": ["parent_id_1", "parent_id_2"],
  "methodeSubdivision": "auto",
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 17. **POST** `/api/eleves/`
Crée un nouvel élève

**Permissions** : Authentifié

**Body (JSON)** :
```json
{
  "nom": "Martin",
  "prenom": "Sophie",
  "matricule": "MAT001",
  "dateNaissance": "2010-05-15T00:00:00Z",
  "classe": "class_id",
  "subdivision": "A",
  "parents": ["parent_id_1"],
  "methodeSubdivision": "auto"
}
```

**Réponse (201 Created)** : Objet Eleve créé

---

#### 18. **PUT** `/api/eleves/<id>/`
Met à jour complètement un élève

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet Eleve mis à jour

---

#### 19. **PATCH** `/api/eleves/<id>/`
Met à jour partiellement un élève

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet Eleve mis à jour

---

#### 20. **DELETE** `/api/eleves/<id>/`
Supprime un élève

**Permissions** : Authentifié

**Réponse (204 No Content)**

---

### 📚 Gestion des Classes

#### 21. **GET** `/api/classes/`
Liste toutes les classes

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets Classe avec structure :
```json
{
  "id": "...",
  "nom": "6ème",
  "niveau": 6,
  "typeClasse": "primaire",
  "seuilPromotion": 10,
  "subdivisions": [],
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 22. **GET** `/api/classes/<id>/`
Récupère une classe par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet Classe

---

#### 23. **POST** `/api/classes/`
Crée une nouvelle classe

**Permissions** : Authentifié

**Body (JSON)** :
```json
{
  "nom": "6ème",
  "niveau": 6,
  "typeClasse": "primaire",
  "seuilPromotion": 10,
  "subdivisions": []
}
```

**Réponse (201 Created)** : Objet Classe créé

---

#### 24. **PUT/PATCH/DELETE** `/api/classes/<id>/`
Opérations CRUD standard

**Permissions** : Authentifié

---

### 📖 Gestion des Matières

#### 25. **GET** `/api/matieres/`
Liste toutes les matières

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets Matiere

---

#### 26. **GET** `/api/matieres/<id>/`
Récupère une matière par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet Matiere avec structure :
```json
{
  "id": "...",
  "nom": "Mathématiques",
  "coefficient": 3,
  "professeur": "prof_id",
  "classe": "class_id",
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 27. **POST** `/api/matieres/`
Crée une nouvelle matière

**Permissions** : Authentifié

**Body (JSON)** :
```json
{
  "nom": "Mathématiques",
  "coefficient": 3,
  "professeur": "prof_id",
  "classe": "class_id"
}
```

**Réponse (201 Created)** : Objet Matiere créé

---

#### 28. **PUT/PATCH/DELETE** `/api/matieres/<id>/`
Opérations CRUD standard

**Permissions** : Authentifié

---

### 📝 Gestion des Devoirs

#### 29. **GET** `/api/devoirs/`
Liste tous les devoirs

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets Devoir

---

#### 30. **GET** `/api/devoirs/<id>/`
Récupère un devoir par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet Devoir avec structure :
```json
{
  "id": "...",
  "titre": "Devoir de Mathématiques",
  "description": "Exercices page 45",
  "dateLimite": "2025-01-30T23:59:00Z",
  "fichier": "url_du_fichier",
  "classe": "class_id",
  "subdivision": "A",
  "matiere": "matiere_id",
  "professeur": "prof_id",
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 31. **POST** `/api/devoirs/`
Crée un nouveau devoir (avec notification automatique aux parents)

**Permissions** : Authentifié

**Body (JSON)** :
```json
{
  "titre": "Devoir de Mathématiques",
  "description": "Exercices page 45",
  "dateLimite": "2025-01-30T23:59:00Z",
  "fichier": "url_du_fichier",
  "classe": "class_id",
  "subdivision": "A",
  "matiere": "matiere_id",
  "professeur": "prof_id"
}
```

**Réponse (201 Created)** : Objet Devoir créé

---

#### 32. **PUT/PATCH/DELETE** `/api/devoirs/<id>/`
Opérations CRUD standard

**Permissions** : Authentifié

---

### 📅 Gestion des Années Scolaires

#### 33. **GET** `/api/annees-scolaires/`
Liste toutes les années scolaires

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets AnneeScolaire

---

#### 34. **GET** `/api/annees-scolaires/<id>/`
Récupère une année scolaire par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet AnneeScolaire avec structure :
```json
{
  "id": "...",
  "nom": "2024-2025",
  "dateDebut": "2024-09-01T00:00:00Z",
  "dateFin": "2025-06-30T00:00:00Z",
  "trimestres": ["trim1_id", "trim2_id", "trim3_id"],
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 35. **POST** `/api/annees-scolaires/`
Crée une nouvelle année scolaire

**Permissions** : Authentifié

**Body (JSON)** :
```json
{
  "nom": "2024-2025",
  "dateDebut": "2024-09-01T00:00:00Z",
  "dateFin": "2025-06-30T00:00:00Z",
  "trimestres": []
}
```

**Réponse (201 Created)** : Objet AnneeScolaire créé

---

#### 36. **PUT/PATCH/DELETE** `/api/annees-scolaires/<id>/`
Opérations CRUD standard

**Permissions** : Authentifié

---

### 📊 Gestion des Trimestres

#### 37. **GET** `/api/trimestres/`
Liste tous les trimestres

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets Trimestre

---

#### 38. **GET** `/api/trimestres/<id>/`
Récupère un trimestre par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet Trimestre avec structure :
```json
{
  "id": "...",
  "nom": "Premier Trimestre",
  "dateDebut": "2024-09-01T00:00:00Z",
  "dateFin": "2024-12-15T00:00:00Z",
  "periodes": ["periode1_id", "periode2_id"],
  "anneeScolaire": "annee_id",
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 39. **POST** `/api/trimestres/`
Crée un nouveau trimestre

**Permissions** : Authentifié

**Body (JSON)** :
```json
{
  "nom": "Premier Trimestre",
  "dateDebut": "2024-09-01T00:00:00Z",
  "dateFin": "2024-12-15T00:00:00Z",
  "periodes": [],
  "anneeScolaire": "annee_id"
}
```

**Réponse (201 Created)** : Objet Trimestre créé

---

#### 40. **PUT/PATCH/DELETE** `/api/trimestres/<id>/`
Opérations CRUD standard

**Permissions** : Authentifié

---

### ⏱️ Gestion des Périodes

#### 41. **GET** `/api/periodes/`
Liste toutes les périodes

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets Periode

---

#### 42. **GET** `/api/periodes/<id>/`
Récupère une période par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet Periode avec structure :
```json
{
  "id": "...",
  "nom": "Période 1",
  "dateDebut": "2024-09-01T00:00:00Z",
  "dateFin": "2024-10-15T00:00:00Z",
  "trimestre": "trimestre_id",
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 43. **POST** `/api/periodes/`
Crée une nouvelle période

**Permissions** : Authentifié

**Body (JSON)** :
```json
{
  "nom": "Période 1",
  "dateDebut": "2024-09-01T00:00:00Z",
  "dateFin": "2024-10-15T00:00:00Z",
  "trimestre": "trimestre_id"
}
```

**Réponse (201 Created)** : Objet Periode créé

---

#### 44. **PUT/PATCH/DELETE** `/api/periodes/<id>/`
Opérations CRUD standard

**Permissions** : Authentifié

---

### 📝 Gestion des Interrogations

#### 45. **GET** `/api/interrogations/`
Liste toutes les interrogations

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets Interrogation

---

#### 46. **GET** `/api/interrogations/<id>/`
Récupère une interrogation par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet Interrogation avec structure :
```json
{
  "id": "...",
  "eleve": "eleve_id",
  "matiere": "matiere_id",
  "periode": "periode_id",
  "note": 15.5,
  "date": "2025-01-15T00:00:00Z",
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 47. **POST** `/api/interrogations/`
Crée une nouvelle interrogation

**Permissions** : Authentifié

**Body (JSON)** :
```json
{
  "eleve": "eleve_id",
  "matiere": "matiere_id",
  "periode": "periode_id",
  "note": 15.5,
  "date": "2025-01-15T00:00:00Z"
}
```

**Réponse (201 Created)** : Objet Interrogation créé

---

#### 48. **PUT/PATCH/DELETE** `/api/interrogations/<id>/`
Opérations CRUD standard

**Permissions** : Authentifié

---

### 📄 Gestion des Examens

#### 49. **GET** `/api/examens/`
Liste tous les examens

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets Examen

---

#### 50. **GET** `/api/examens/<id>/`
Récupère un examen par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet Examen avec structure :
```json
{
  "id": "...",
  "eleve": "eleve_id",
  "matiere": "matiere_id",
  "trimestre": "trimestre_id",
  "note": 16.0,
  "date": "2025-01-20T00:00:00Z",
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 51. **POST** `/api/examens/`
Crée un nouvel examen

**Permissions** : Authentifié

**Body (JSON)** :
```json
{
  "eleve": "eleve_id",
  "matiere": "matiere_id",
  "trimestre": "trimestre_id",
  "note": 16.0,
  "date": "2025-01-20T00:00:00Z"
}
```

**Réponse (201 Created)** : Objet Examen créé

---

#### 52. **PUT/PATCH/DELETE** `/api/examens/<id>/`
Opérations CRUD standard

**Permissions** : Authentifié

---

### 📊 Notes Trimestrielles

#### 53. **GET** `/api/notes-trimestrielles/`
Liste toutes les notes trimestrielles

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets NoteTrimestrielle

---

#### 54. **GET** `/api/notes-trimestrielles/<id>/`
Récupère une note trimestrielle par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet NoteTrimestrielle avec structure :
```json
{
  "id": "...",
  "eleve": "eleve_id",
  "matiere": "matiere_id",
  "trimestre": "trimestre_id",
  "noteFinale": 15.75,
  "details": {
    "moyenneTravaux": 15.5,
    "noteExamen": 16.0
  },
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 55. **POST** `/api/notes-trimestrielles/`
Crée une nouvelle note trimestrielle

**Permissions** : Authentifié

**Body (JSON)** :
```json
{
  "eleve": "eleve_id",
  "matiere": "matiere_id",
  "trimestre": "trimestre_id",
  "noteFinale": 15.75,
  "details": {
    "moyenneTravaux": 15.5,
    "noteExamen": 16.0
  }
}
```

**Réponse (201 Created)** : Objet NoteTrimestrielle créé

---

#### 56. **PUT/PATCH/DELETE** `/api/notes-trimestrielles/<id>/`
Opérations CRUD standard

**Permissions** : Authentifié

---

### 📈 Notes Annuelles

#### 57. **GET** `/api/notes-annuelles/`
Liste toutes les notes annuelles

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets NoteAnnuelle

---

#### 58. **GET** `/api/notes-annuelles/<id>/`
Récupère une note annuelle par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet NoteAnnuelle avec structure :
```json
{
  "id": "...",
  "eleve": "eleve_id",
  "matiere": "matiere_id",
  "anneeScolaire": "annee_id",
  "noteFinale": 16.0,
  "details": [
    {
      "trimestre": "trim1_id",
      "noteTrimestre": 15.5
    },
    {
      "trimestre": "trim2_id",
      "noteTrimestre": 16.0
    },
    {
      "trimestre": "trim3_id",
      "noteTrimestre": 16.5
    }
  ],
  "promotionAutomatique": true,
  "nouvelleClasse": "class_id",
  "nouvelleSubdivision": "B",
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 59. **POST** `/api/notes-annuelles/`
Crée une nouvelle note annuelle

**Permissions** : Authentifié

**Body (JSON)** : Structure similaire à la réponse GET

**Réponse (201 Created)** : Objet NoteAnnuelle créé

---

#### 60. **PUT/PATCH/DELETE** `/api/notes-annuelles/<id>/`
Opérations CRUD standard

**Permissions** : Authentifié

---

### 💬 Gestion des Messages

#### 61. **GET** `/api/messages/`
Liste tous les messages

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets Message

---

#### 62. **GET** `/api/messages/<id>/`
Récupère un message par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet Message avec structure :
```json
{
  "id": "...",
  "sender": "sender_id",
  "receiver": "receiver_id",
  "contenu": "Bonjour, je souhaite discuter des résultats de mon enfant.",
  "lu": false,
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 63. **POST** `/api/messages/`
Crée un nouveau message (avec notification automatique au destinataire)

**Permissions** : Authentifié

**Body (JSON)** :
```json
{
  "sender": "sender_id",
  "receiver": "receiver_id",
  "contenu": "Bonjour, je souhaite discuter des résultats de mon enfant."
}
```

**Réponse (201 Created)** : Objet Message créé

---

#### 64. **PUT/PATCH/DELETE** `/api/messages/<id>/`
Opérations CRUD standard

**Permissions** : Authentifié

---

### 🔔 Gestion des Notifications

#### 65. **GET** `/api/notifications/`
Liste toutes les notifications de l'utilisateur connecté

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets Notification (filtrées par destinataire)

---

#### 66. **GET** `/api/notifications/<id>/`
Récupère une notification par ID (uniquement si destinée à l'utilisateur connecté)

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet Notification avec structure :
```json
{
  "id": "...",
  "destinataire": "user_id",
  "type": "devoir",
  "referenceId": "devoir_id",
  "lu": false,
  "dateEnvoi": "2025-01-15T10:30:00Z",
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 67. **POST** `/api/notifications/`
Crée une nouvelle notification

**Permissions** : Authentifié

**Body (JSON)** :
```json
{
  "destinataire": "user_id",
  "type": "devoir",
  "referenceId": "devoir_id",
  "dateEnvoi": "2025-01-15T10:30:00Z"
}
```

**Réponse (201 Created)** : Objet Notification créé

---

#### 68. **PUT/PATCH/DELETE** `/api/notifications/<id>/`
Opérations CRUD standard

**Permissions** : Authentifié

---

### 📅 Gestion des Emplois du Temps

#### 69. **GET** `/api/emplois-du-temps/`
Liste tous les emplois du temps

**Permissions** : Authentifié

**Réponse (200 OK)** : Liste d'objets EmploiDuTemps

---

#### 70. **GET** `/api/emplois-du-temps/<id>/`
Récupère un emploi du temps par ID

**Permissions** : Authentifié

**Réponse (200 OK)** : Objet EmploiDuTemps avec structure :
```json
{
  "id": "...",
  "classe": "class_id",
  "subdivision": "A",
  "anneeScolaire": "annee_id",
  "fixe": true,
  "jours": [
    {
      "nom": "Lundi",
      "cours": [
        {
          "heureDebut": "08:00",
          "heureFin": "09:00",
          "matiere": "matiere_id",
          "professeur": "prof_id",
          "isPause": false
        },
        {
          "heureDebut": "09:00",
          "heureFin": "09:15",
          "isPause": true
        }
      ]
    }
  ],
  "createdAt": "...",
  "updatedAt": "..."
}
```

---

#### 71. **POST** `/api/emplois-du-temps/`
Crée un nouvel emploi du temps

**Permissions** : Authentifié

**Body (JSON)** : Structure similaire à la réponse GET

**Réponse (201 Created)** : Objet EmploiDuTemps créé

---

#### 72. **PUT/PATCH/DELETE** `/api/emplois-du-temps/<id>/`
Opérations CRUD standard

**Permissions** : Authentifié

---

### ⚙️ Opérations Complexes

#### 73. **POST** `/api/calcul-notes-trimestrielles/`
Calcul automatique des notes trimestrielles

**Permissions** : Authentifié (admin, developpeur, professeur)

**Headers** :
```
Authorization: Token <votre_token>
```

**Body (JSON)** :
```json
{
  "trimestre_id": "trimestre_id"
}
```

**Réponse (200 OK)** :
```json
{
  "message": "X notes calculées"
}
```

**Fonctionnalité** : Calcule automatiquement les notes trimestrielles pour tous les élèves et toutes les matières du trimestre spécifié.

**Formule** : `noteFinale = (moyenneTravaux * 0.5) + (noteExamen * 0.5)`

---

#### 74. **POST** `/api/promotion-automatique/`
Promotion automatique des élèves

**Permissions** : Authentifié (admin, developpeur)

**Headers** :
```
Authorization: Token <votre_token>
```

**Body (JSON)** :
```json
{
  "annee_scolaire_id": "annee_id",
  "methode_subdivision": "auto"  // "auto" | "manuel"
}
```

**Réponse (200 OK)** :
```json
{
  "message": "Promotion automatique terminée",
  "promotions_reussies": 25,
  "promotions_echouees": 5
}
```

**Fonctionnalité** : Promouvoit automatiquement les élèves en fonction de leur note annuelle et du seuil de promotion de leur classe.

---

#### 75. **POST** `/api/affecter-parent/`
Affecter un ou plusieurs élèves à un parent

**Permissions** : Authentifié (admin, developpeur, professeur)

**Headers** :
```
Authorization: Token <votre_token>
```

**Body (JSON)** :
```json
{
  "parent_id": "parent_id",
  "eleve_ids": ["eleve_id_1", "eleve_id_2", "eleve_id_3"]
}
```

**Réponse (200 OK)** :
```json
{
  "message": "Affecté 3 élève(s) au parent Jean Dupont",
  "assigned": [
    {
      "eleve_id": "eleve_id_1",
      "eleve_nom": "Sophie Martin"
    },
    {
      "eleve_id": "eleve_id_2",
      "eleve_nom": "Pierre Martin"
    }
  ],
  "errors": []  // Si des erreurs sont survenues
}
```

---

#### 76. **POST** `/api/gestion-notifications/`
Marquer toutes les notifications comme lues

**Permissions** : Authentifié

**Headers** :
```
Authorization: Token <votre_token>
```

**Réponse (200 OK)** :
```json
{
  "message": "X notifications marquées comme lues"
}
```

---

#### 77. **PATCH** `/api/marquer-notification-lue/<id>/`
Marquer une notification spécifique comme lue

**Permissions** : Authentifié

**Headers** :
```
Authorization: Token <votre_token>
```

**Réponse (200 OK)** :
```json
{
  "status": "notification marquée comme lue"
}
```

---

### 📖 Documentation Swagger/OpenAPI

#### 78. **GET** `/api/schema/`
Schéma OpenAPI de l'API

**Permissions** : Aucune

---

#### 79. **GET** `/api/schema/swagger-ui/`
Interface Swagger UI pour tester l'API

**Permissions** : Aucune

---

#### 80. **GET** `/api/schema/redoc/`
Documentation ReDoc de l'API

**Permissions** : Aucune

---

## 📊 Récapitulatif des Modèles de Données

### User
- `id` (ObjectId)
- `nom` (String)
- `prenom` (String)
- `email` (String, unique)
- `motDePasse` (String, hashed)
- `role` (String: "parent" | "professeur" | "admin" | "developpeur")
- `telephone` (String)
- `enfants` (List[ReferenceField(Eleve)])

### Eleve
- `id` (ObjectId)
- `nom` (String)
- `prenom` (String)
- `matricule` (String, unique)
- `dateNaissance` (DateTime)
- `classe` (ReferenceField(Classe))
- `subdivision` (String)
- `parents` (List[ReferenceField(User)])
- `methodeSubdivision` (String: "auto" | "manuel")

### Classe
- `id` (ObjectId)
- `nom` (String)
- `niveau` (Integer)
- `typeClasse` (String: "primaire" | "secondaire")
- `seuilPromotion` (Integer)
- `subdivisions` (List[EmbeddedDocument(Subdivision)])

### Matiere
- `id` (ObjectId)
- `nom` (String)
- `coefficient` (Integer)
- `professeur` (ReferenceField(User))
- `classe` (ReferenceField(Classe))

### Devoir
- `id` (ObjectId)
- `titre` (String)
- `description` (String)
- `dateLimite` (DateTime)
- `fichier` (String)
- `classe` (ReferenceField(Classe))
- `subdivision` (String)
- `matiere` (ReferenceField(Matiere))
- `professeur` (ReferenceField(User))

### NoteTrimestrielle
- `id` (ObjectId)
- `eleve` (ReferenceField(Eleve))
- `matiere` (ReferenceField(Matiere))
- `trimestre` (ReferenceField(Trimestre))
- `noteFinale` (Float)
- `details` (EmbeddedDocument: {moyenneTravaux, noteExamen})

### NoteAnnuelle
- `id` (ObjectId)
- `eleve` (ReferenceField(Eleve))
- `matiere` (ReferenceField(Matiere))
- `anneeScolaire` (ReferenceField(AnneeScolaire))
- `noteFinale` (Float)
- `details` (List[EmbeddedDocument: {trimestre, noteTrimestre}])
- `promotionAutomatique` (Boolean)
- `nouvelleClasse` (ReferenceField(Classe))
- `nouvelleSubdivision` (String)

---

## 🔒 Permissions par Rôle

### Développeur
- ✅ Accès complet à toutes les fonctionnalités
- ✅ Gestion des utilisateurs et rôles

### Administrateur
- ✅ Gestion complète de toutes les entités
- ✅ Configuration des emplois du temps
- ✅ Promotion automatique
- ✅ Consultation de toutes les données

### Professeur
- ✅ Saisie/modification des notes pendant les périodes actives
- ✅ Consultation des résultats de sa subdivision
- ✅ Envoi/réception de messages
- ✅ Création de devoirs
- ✅ Calcul des notes trimestrielles

### Parent
- ✅ Consultation des résultats de ses enfants
- ✅ Consultation des emplois du temps
- ✅ Réception de notifications et messages
- ✅ Communication avec les professeurs

---

## 🛠️ Technologies Utilisées

- **Django** 5.2.7
- **Django REST Framework** 3.16.1
- **MongoDB** (via MongoEngine 0.29.1)
- **PyMongo** 4.15.2
- **DRF Spectacular** 0.28.0 (Documentation OpenAPI)
- **django-cors-headers** 4.9.0 (CORS)

---

## 📝 Notes Importantes

1. **Authentification** : Utilise des tokens personnalisés stockés dans MongoDB (modèle `AuthToken`)
2. **Base de données** : MongoDB Atlas (configuré dans `settings.py`)
3. **Format des dates** : ISO 8601 (ex: "2025-01-15T10:30:00Z")
4. **IDs** : Utilisation d'ObjectId MongoDB (chaînes de caractères)
5. **Notifications automatiques** : Créées lors de la création de devoirs et messages
6. **Calcul des notes** : Automatique via les services (`NoteService`)

---

## 🚨 Codes de Statut HTTP

- **200 OK** : Requête réussie
- **201 Created** : Ressource créée avec succès
- **204 No Content** : Suppression réussie
- **400 Bad Request** : Données invalides
- **401 Unauthorized** : Non authentifié
- **403 Forbidden** : Permissions insuffisantes
- **404 Not Found** : Ressource non trouvée
- **500 Internal Server Error** : Erreur serveur

---

**Version de la documentation** : 1.0.0  
**Date** : Janvier 2025

