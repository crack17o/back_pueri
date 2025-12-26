
# Utilisation de mongoengine pour MongoDB
import mongoengine as me
from datetime import datetime

# Mixin pour auto-compléter les dates
class TimestampMixin:
    def save(self, *args, **kwargs):
        if not self.createdAt:
            self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()
        return super().save(*args, **kwargs)

# User
class User(me.Document, TimestampMixin):
    nom = me.StringField(required=True)
    prenom = me.StringField(required=True)
    email = me.StringField(required=True, unique=True)
    motDePasse = me.StringField(required=True)
    role = me.StringField(choices=["parent","professeur","admin","developpeur"], required=True)
    telephone = me.StringField()
    enfants = me.ListField(me.ReferenceField('Eleve'))
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()
    
    # Attributs requis pour Django REST Framework
    @property
    def is_authenticated(self):
        """Toujours retourner True pour les utilisateu rs authentifiés"""
        return True
    
    @property
    def is_anonymous(self):
        """Toujours retourner False - pas d'utilisateurs anonymes"""
        return False
    
    @property
    def is_active(self):
        """Toujours actif pour le moment"""
        return True
    
    @property
    def is_staff(self):
        """Staff si admin ou développeur"""
        return self.role in ['admin', 'developpeur']
    
    @property
    def is_superuser(self):
        """Superuser si développeur"""
        return self.role == 'developpeur'
    
    def get_username(self):
        return self.email
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.email})"

#Eleve
class Eleve(me.Document, TimestampMixin):
	nom = me.StringField(required=True)
	prenom = me.StringField(required=True)
	matricule = me.StringField(required=True, unique=True)
	dateNaissance = me.DateTimeField()
	classe = me.ReferenceField('Classe')
	subdivision = me.StringField()
	parents = me.ListField(me.ReferenceField('User'))
	methodeSubdivision = me.StringField(choices=["auto","manuel"])
	createdAt = me.DateTimeField()
	updatedAt = me.DateTimeField()

# Embedded Document pour les subdivisions
class Subdivision(me.EmbeddedDocument):
	nom = me.StringField()
	profPrincipal = me.ReferenceField('User')

#Classe
class Classe(me.Document, TimestampMixin):
	nom = me.StringField(required=True)
	niveau = me.IntField(required=True)
	typeClasse = me.StringField(choices=["primaire","secondaire"], required=True)
	seuilPromotion = me.IntField()
	subdivisions = me.ListField(me.EmbeddedDocumentField(Subdivision))
	createdAt = me.DateTimeField()
	updatedAt = me.DateTimeField()

#Matiere
class Matiere(me.Document, TimestampMixin):
    nom = me.StringField(required=True)
    coefficient = me.IntField()
    professeur = me.ReferenceField('User')
    classe = me.ReferenceField('Classe')
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()

#Devoir
class Devoir(me.Document, TimestampMixin):
    titre = me.StringField(required=True)
    description = me.StringField()
    dateLimite = me.DateTimeField()
    fichier = me.StringField()
    classe = me.ReferenceField('Classe')
    subdivision = me.StringField()
    matiere = me.ReferenceField('Matiere')
    professeur = me.ReferenceField('User')
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()

#AnneeScolaire
class AnneeScolaire(me.Document, TimestampMixin):
    nom = me.StringField(required=True)
    dateDebut = me.DateTimeField()
    dateFin = me.DateTimeField()
    trimestres = me.ListField(me.ReferenceField('Trimestre'))
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()

#Trimestre
class Trimestre(me.Document, TimestampMixin):
    nom = me.StringField(required=True)
    dateDebut = me.DateTimeField()
    dateFin = me.DateTimeField()
    periodes = me.ListField(me.ReferenceField('Periode'))
    anneeScolaire = me.ReferenceField('AnneeScolaire')
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()

#Periode
class Periode(me.Document, TimestampMixin):
    nom = me.StringField(required=True)
    dateDebut = me.DateTimeField()
    dateFin = me.DateTimeField()
    trimestre = me.ReferenceField('Trimestre')
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()

#Interrogation
class Interrogation(me.Document, TimestampMixin):
    eleve = me.ReferenceField('Eleve')
    matiere = me.ReferenceField('Matiere')
    periode = me.ReferenceField('Periode')
    note = me.FloatField()
    date = me.DateTimeField()
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()

#Examen
class Examen(me.Document, TimestampMixin):
    eleve = me.ReferenceField('Eleve')
    matiere = me.ReferenceField('Matiere')
    trimestre = me.ReferenceField('Trimestre')
    note = me.FloatField()
    date = me.DateTimeField()
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()

#NoteTrimestrielle
class DetailsNoteTrimestrielle(me.EmbeddedDocument):
    moyenneTravaux = me.FloatField()
    noteExamen = me.FloatField()

class NoteTrimestrielle(me.Document, TimestampMixin):
    eleve = me.ReferenceField('Eleve')
    matiere = me.ReferenceField('Matiere')
    trimestre = me.ReferenceField('Trimestre')
    noteFinale = me.FloatField()
    details = me.EmbeddedDocumentField('DetailsNoteTrimestrielle')
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()

#NoteAnnuelle
class DetailNoteAnnuelle(me.EmbeddedDocument):
    trimestre = me.ReferenceField('Trimestre')
    noteTrimestre = me.FloatField()

class NoteAnnuelle(me.Document, TimestampMixin):
    eleve = me.ReferenceField('Eleve')
    matiere = me.ReferenceField('Matiere')
    anneeScolaire = me.ReferenceField('AnneeScolaire')
    noteFinale = me.FloatField()
    details = me.ListField(me.EmbeddedDocumentField('DetailNoteAnnuelle'))
    promotionAutomatique = me.BooleanField(default=False)
    nouvelleClasse = me.ReferenceField('Classe')
    nouvelleSubdivision = me.StringField()
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()

#Message
class Message(me.Document, TimestampMixin):
    sender = me.ReferenceField('User')
    receiver = me.ReferenceField('User')
    contenu = me.StringField()
    lu = me.BooleanField(default=False)
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()

#Notification
class Notification(me.Document, TimestampMixin):
    destinataire = me.ReferenceField('User')
    type = me.StringField(choices=["message","devoir"])
    referenceId = me.ObjectIdField()
    lu = me.BooleanField(default=False)
    dateEnvoi = me.DateTimeField()
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()

#EmploiDuTemps
class CoursEmploi(me.EmbeddedDocument):
    heureDebut = me.StringField()
    heureFin = me.StringField()
    matiere = me.ReferenceField('Matiere')  # ou "Pause" pour les pauses
    professeur = me.ReferenceField('User')  # facultatif si Pause
    isPause = me.BooleanField(default=False)  # True pour les cours "Pause"

class JourEmploi(me.EmbeddedDocument):
    nom = me.StringField(choices=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi"])
    cours = me.ListField(me.EmbeddedDocumentField('CoursEmploi'))

class EmploiDuTemps(me.Document, TimestampMixin):
    classe = me.ReferenceField('Classe')
    subdivision = me.StringField()
    anneeScolaire = me.ReferenceField('AnneeScolaire')
    fixe = me.BooleanField(default=True)
    jours = me.ListField(me.EmbeddedDocumentField('JourEmploi'))
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()

# 16️⃣ Token d'authentification personnalisé
class AuthToken(me.Document, TimestampMixin):
    key = me.StringField(required=True, unique=True, max_length=40)
    user = me.ReferenceField('User', required=True)
    created = me.DateTimeField()
    createdAt = me.DateTimeField()
    updatedAt = me.DateTimeField()
    
    @staticmethod
    def generate_key():
        """Génère une clé de token unique"""
        import secrets
        return secrets.token_hex(20)  # 40 caractères hexadécimaux
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        if not self.created:
            self.created = datetime.utcnow()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Token for {self.user.email}"