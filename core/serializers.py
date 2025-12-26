from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import (
    User, Eleve, Classe, Matiere, Devoir, AnneeScolaire, 
    Trimestre, Periode, Interrogation, Examen, NoteTrimestrielle, 
    NoteAnnuelle, Message, Notification, EmploiDuTemps, AuthToken
)

# Serializers d'authentification
class UserRegistrationSerializer(serializers.Serializer):
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    motDePasse = serializers.CharField(min_length=6, write_only=True)
    role = serializers.ChoiceField(choices=["parent","professeur","admin","developpeur"], default='parent')
    telephone = serializers.CharField(max_length=20, required=False)
    
    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError("Un utilisateur avec cet email existe déjà.")
        return value
    
    def create(self, validated_data):
        validated_data['motDePasse'] = make_password(validated_data['motDePasse'])
        user = User(**validated_data)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    motDePasse = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        motDePasse = data.get('motDePasse')
        print(motDePasse)
        if email and motDePasse:
            try:
                user = User.objects.get(email=email)
                if not check_password(motDePasse, user.motDePasse):
                    raise serializers.ValidationError("Mot de passe incorrect.")
            except User.DoesNotExist:
                raise serializers.ValidationError("Utilisateur introuvable.")
            
            data['user'] = user
        else:
            raise serializers.ValidationError("Email et mot de passe requis.")
        
        return data

class UserProfileSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField(read_only=True)  # Email non modifiable
    role = serializers.CharField(read_only=True)   # Rôle non modifiable
    telephone = serializers.CharField(max_length=20, required=False)
    enfants = serializers.ListField(read_only=True)
    
    def update(self, instance, validated_data):
        instance.nom = validated_data.get('nom', instance.nom)
        instance.prenom = validated_data.get('prenom', instance.prenom)
        instance.telephone = validated_data.get('telephone', instance.telephone)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    ancien_mot_de_passe = serializers.CharField(write_only=True)
    nouveau_mot_de_passe = serializers.CharField(min_length=6, write_only=True)
    
    def validate_ancien_mot_de_passe(self, value):
        user = self.context['request'].user
        if not check_password(value, user.motDePasse):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")
        return value
    
    def save(self):
        user = self.context['request'].user
        user.motDePasse = make_password(self.validated_data['nouveau_mot_de_passe'])
        user.save()
        return user

# Serializers personnalisés pour MongoDB avec mongoengine
class BaseMongoSerializer(serializers.Serializer):
    """Base serializer pour mongoengine documents"""
    def create(self, validated_data):
        return self.Meta.model(**validated_data).save()
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# Serializer pour les tokens
class AuthTokenSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    key = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = AuthToken
        fields = ['id', 'key', 'user', 'created']
class BaseMongoSerializer(serializers.Serializer):
    """Base serializer pour mongoengine documents"""
    def create(self, validated_data):
        return self.Meta.model(**validated_data).save()
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UserSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    motDePasse = serializers.CharField(write_only=True, max_length=128)
    role = serializers.ChoiceField(choices=["parent","professeur","admin","developpeur"])
    telephone = serializers.CharField(max_length=20, required=False)
    enfants = serializers.ListField(child=serializers.CharField(), required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = User

class EleveSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    matricule = serializers.CharField(max_length=50)
    dateNaissance = serializers.DateTimeField()
    classe = serializers.CharField(required=False)
    subdivision = serializers.CharField(max_length=10, required=False)
    parents = serializers.ListField(child=serializers.CharField(), required=False)
    methodeSubdivision = serializers.ChoiceField(choices=["auto","manuel"], required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Eleve

class ClasseSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    niveau = serializers.IntegerField()
    typeClasse = serializers.ChoiceField(choices=["primaire","secondaire"])
    seuilPromotion = serializers.IntegerField(required=False)
    subdivisions = serializers.ListField(required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Classe

class MatiereSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    coefficient = serializers.IntegerField(required=False)
    professeur = serializers.CharField(required=False)
    classe = serializers.CharField(required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Matiere

class DevoirSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    titre = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False)
    dateLimite = serializers.DateTimeField(required=False)
    fichier = serializers.CharField(required=False)
    classe = serializers.CharField(required=False)
    subdivision = serializers.CharField(max_length=10, required=False)
    matiere = serializers.CharField(required=False)
    professeur = serializers.CharField(required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Devoir

class AnneeScolaireSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    dateDebut = serializers.DateTimeField(required=False)
    dateFin = serializers.DateTimeField(required=False)
    trimestres = serializers.ListField(child=serializers.CharField(), required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = AnneeScolaire

class TrimestreSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    dateDebut = serializers.DateTimeField(required=False)
    dateFin = serializers.DateTimeField(required=False)
    periodes = serializers.ListField(child=serializers.CharField(), required=False)
    anneeScolaire = serializers.CharField(required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Trimestre

class PeriodeSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    dateDebut = serializers.DateTimeField(required=False)
    dateFin = serializers.DateTimeField(required=False)
    trimestre = serializers.CharField(required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Periode

class InterrogationSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    eleve = serializers.CharField(required=False)
    matiere = serializers.CharField(required=False)
    periode = serializers.CharField(required=False)
    note = serializers.FloatField(required=False)
    date = serializers.DateTimeField(required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Interrogation

class ExamenSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    eleve = serializers.CharField(required=False)
    matiere = serializers.CharField(required=False)
    trimestre = serializers.CharField(required=False)
    note = serializers.FloatField(required=False)
    date = serializers.DateTimeField(required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Examen

class NoteTrimestrielleSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    eleve = serializers.CharField(required=False)
    matiere = serializers.CharField(required=False)
    trimestre = serializers.CharField(required=False)
    noteFinale = serializers.FloatField(required=False)
    details = serializers.DictField(required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = NoteTrimestrielle

class NoteAnnuelleSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    eleve = serializers.CharField(required=False)
    matiere = serializers.CharField(required=False)
    anneeScolaire = serializers.CharField(required=False)
    noteFinale = serializers.FloatField(required=False)
    details = serializers.ListField(required=False)
    promotionAutomatique = serializers.BooleanField(default=False)
    nouvelleClasse = serializers.CharField(required=False)
    nouvelleSubdivision = serializers.CharField(max_length=10, required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = NoteAnnuelle

class MessageSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    sender = serializers.CharField(required=False)
    receiver = serializers.CharField(required=False)
    contenu = serializers.CharField()
    lu = serializers.BooleanField(default=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Message

class NotificationSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    destinataire = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=["message","devoir"])
    referenceId = serializers.CharField(required=False)
    lu = serializers.BooleanField(default=False)
    dateEnvoi = serializers.DateTimeField(required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Notification

class EmploiDuTempsSerializer(BaseMongoSerializer):
    id = serializers.CharField(read_only=True)
    classe = serializers.CharField(required=False)
    subdivision = serializers.CharField(max_length=10, required=False)
    anneeScolaire = serializers.CharField(required=False)
    fixe = serializers.BooleanField(default=True)
    jours = serializers.ListField(required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = EmploiDuTemps
