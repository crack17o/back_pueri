from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import check_password
from django.utils import timezone
import random

from .models import (
    User, Eleve, Classe, Matiere, Devoir, AnneeScolaire, 
    Trimestre, Periode, Interrogation, Examen, NoteTrimestrielle, 
    NoteAnnuelle, Message, Notification, EmploiDuTemps
)
from .serializers import (
    UserSerializer, EleveSerializer, ClasseSerializer, MatiereSerializer,
    DevoirSerializer, AnneeScolaireSerializer, TrimestreSerializer, 
    PeriodeSerializer, InterrogationSerializer, ExamenSerializer,
    NoteTrimestrielleSerializer, NoteAnnuelleSerializer, MessageSerializer,
    NotificationSerializer, EmploiDuTempsSerializer,
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, ChangePasswordSerializer
)
from .services import NoteService, PromotionService, NotificationService, AuthTokenService
try:
    from .permissions import (
        IsDeveloppeur, IsAdmin, IsProfesseur, IsParent,
        CanManageUsers, CanManageEleves, CanManageNotes
    )
except ImportError:
    # Permissions par défaut si le fichier permissions.py n'existe pas
    IsDeveloppeur = IsAuthenticated
    IsAdmin = IsAuthenticated
    IsProfesseur = IsAuthenticated
    IsParent = IsAuthenticated
    CanManageUsers = IsAuthenticated
    CanManageEleves = IsAuthenticated
    CanManageNotes = IsAuthenticated

# ============ VUES D'AUTHENTIFICATION ============

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Inscription d'un nouvel utilisateur"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Créer un token pour l'utilisateur
        token = AuthTokenService.create_token(user)
        return Response({
            'message': 'Utilisateur créé avec succès',
            'user': {
                'id': str(user.id),
                'nom': user.nom,
                'prenom': user.prenom,
                'email': user.email,
                'role': user.role
            },
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Connexion d'un utilisateur"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        # Créer un token pour l'utilisateur
        token = AuthTokenService.create_token(user)
        return Response({
            'message': 'Connexion réussie',
            'user': {
                'id': str(user.id),
                'nom': user.nom,
                'prenom': user.prenom,
                'email': user.email,
                'role': user.role,
                'telephone': user.telephone
            },
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Déconnexion d'un utilisateur"""
    # Récupérer le token de l'en-tête Authorization
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if auth_header.startswith('Token '):
        token_key = auth_header.split(' ')[1]
        if AuthTokenService.delete_token(token_key):
            return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)
    
    return Response({'message': 'Erreur lors de la déconnexion'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Consultation et modification du profil utilisateur"""
    user = request.user
    
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profil mis à jour avec succès',
                'user': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Changement de mot de passe"""
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Mot de passe modifié avec succès'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def token_info(request):
    """Informations sur le token actuel"""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if auth_header.startswith('Token '):
        token_key = auth_header.split(' ')[1]
        from .models import AuthToken
        try:
            token = AuthToken.objects.get(key=token_key)
            return Response({
                'token_key': token.key[:10] + '...',  # Masquer une partie du token
                'created': token.created,
                'user': {
                    'id': str(token.user.id),
                    'email': token.user.email,
                    'role': token.user.role
                }
            })
        except AuthToken.DoesNotExist:
            return Response({'error': 'Token invalide'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Aucun token fourni'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    """Actualiser le token (créer un nouveau token)"""
    # Supprimer l'ancien token
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if auth_header.startswith('Token '):
        old_token_key = auth_header.split(' ')[1]
        AuthTokenService.delete_token(old_token_key)
    
    # Créer un nouveau token
    new_token = AuthTokenService.create_token(request.user)
    
    return Response({
        'message': 'Token actualisé avec succès',
        'token': new_token.key
    })

# ============ VIEWSETS POUR L'API REST ============
    CanManageUsers = IsAuthenticated
    CanManageEleves = IsAuthenticated
    CanManageNotes = IsAuthenticated

# Base ViewSet personnalisé pour mongoengine
class MongoViewSet(viewsets.ViewSet):
    """ViewSet personnalisé pour mongoengine documents"""
    queryset = None
    serializer_class = None
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class([obj for obj in queryset], many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            obj = self.queryset.objects.get(id=pk)
            serializer = self.serializer_class(obj)
            return Response(serializer.data)
        except self.queryset.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        try:
            obj = self.queryset.objects.get(id=pk)
            serializer = self.serializer_class(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except self.queryset.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        try:
            obj = self.queryset.objects.get(id=pk)
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except self.queryset.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UserViewSet(MongoViewSet):
    queryset = User
    serializer_class = UserSerializer

class EleveViewSet(MongoViewSet):
    queryset = Eleve
    serializer_class = EleveSerializer

class ClasseViewSet(MongoViewSet):
    queryset = Classe
    serializer_class = ClasseSerializer

class MatiereViewSet(MongoViewSet):
    queryset = Matiere
    serializer_class = MatiereSerializer

class DevoirViewSet(MongoViewSet):
    queryset = Devoir
    serializer_class = DevoirSerializer
    
    def create(self, request, *args, **kwargs):
        """Créer un devoir et envoyer des notifications automatiques"""
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            # Créer des notifications pour les parents
            devoir_id = response.data['id']
            NotificationService.creer_notification_devoir(devoir_id)
        return response

class AnneeScolaireViewSet(MongoViewSet):
    queryset = AnneeScolaire
    serializer_class = AnneeScolaireSerializer

class TrimestreViewSet(MongoViewSet):
    queryset = Trimestre
    serializer_class = TrimestreSerializer

class PeriodeViewSet(MongoViewSet):
    queryset = Periode
    serializer_class = PeriodeSerializer

class InterrogationViewSet(MongoViewSet):
    queryset = Interrogation
    serializer_class = InterrogationSerializer

class ExamenViewSet(MongoViewSet):
    queryset = Examen
    serializer_class = ExamenSerializer

class NoteTrimestrielleViewSet(MongoViewSet):
    queryset = NoteTrimestrielle
    serializer_class = NoteTrimestrielleSerializer
    
    @action(detail=False, methods=['post'])
    def calculer_notes_trimestrielles(self, request):
        """Calcul automatique des notes trimestrielles : 50% travaux + 50% examens"""
        if not (request.user.role in ['admin', 'developpeur', 'professeur']):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        trimestre_id = request.data.get('trimestre_id')
        if not trimestre_id:
            return Response({'error': 'trimestre_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            trimestre = Trimestre.objects.get(id=trimestre_id)
            eleves = Eleve.objects.all()
            matieres = Matiere.objects.all()
            
            notes_calculees = 0
            for eleve in eleves:
                for matiere in matieres:
                    resultat = NoteService.calculer_note_trimestrielle(
                        str(eleve.id), str(matiere.id), trimestre_id
                    )
                    
                    note_trim, created = NoteTrimestrielle.objects.get_or_create(
                        eleve=eleve,
                        matiere=matiere,
                        trimestre=trimestre,
                        defaults={
                            'noteFinale': resultat['note_finale'],
                            'details': {
                                'moyenneTravaux': resultat['moyenne_travaux'],
                                'noteExamen': resultat['note_examen']
                            }
                        }
                    )
                    
                    if not created:
                        note_trim.noteFinale = resultat['note_finale']
                        note_trim.save()
                    
                    notes_calculees += 1
            
            return Response({'message': f'{notes_calculees} notes calculées'})
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class NoteAnnuelleViewSet(MongoViewSet):
    queryset = NoteAnnuelle
    serializer_class = NoteAnnuelleSerializer
    
    @action(detail=False, methods=['post'])
    def promotion_automatique(self, request):
        """Promotion automatique des élèves ayant atteint le seuil"""
        if not (request.user.role in ['admin', 'developpeur']):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        annee_id = request.data.get('annee_scolaire_id')
        methode_subdivision = request.data.get('methode_subdivision', 'auto')
        
        if not annee_id:
            return Response({'error': 'annee_scolaire_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            eleves = Eleve.objects.all()
            promotions_reussies = 0
            promotions_echouees = 0
            
            for eleve in eleves:
                resultat = PromotionService.promouvoir_eleve(
                    str(eleve.id), annee_id, methode_subdivision
                )
                
                if resultat['promotion_effectuee']:
                    promotions_reussies += 1
                else:
                    promotions_echouees += 1
            
            return Response({
                'message': 'Promotion automatique terminée',
                'promotions_reussies': promotions_reussies,
                'promotions_echouees': promotions_echouees
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(MongoViewSet):
    queryset = Message
    serializer_class = MessageSerializer
    
    def create(self, request, *args, **kwargs):
        """Créer un message et envoyer une notification automatique"""
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            # Créer une notification pour le destinataire
            message_id = response.data['id']
            NotificationService.creer_notification_message(message_id)
        return response

class NotificationViewSet(MongoViewSet):
    queryset = Notification
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(destinataire=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def marquer_lu(self, request, pk=None):
        """Marquer une notification comme lue"""
        try:
            notification = Notification.objects.get(id=pk, destinataire=request.user)
            notification.lu = True
            notification.save()
            return Response({'status': 'notification marquée comme lue'})
        except Notification.DoesNotExist:
            return Response({'error': 'Notification introuvable'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def marquer_toutes_lues(self, request):
        """Marquer toutes les notifications comme lues"""
        result = NotificationService.marquer_notifications_lues(str(request.user.id))
        return Response(result)

class EmploiDuTempsViewSet(MongoViewSet):
    queryset = EmploiDuTemps
    serializer_class = EmploiDuTempsSerializer
