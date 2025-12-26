from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import check_password
from django.utils import timezone
import random

from .models import (
    User,
    Eleve,
    Classe,
    Matiere,
    Devoir,
    AnneeScolaire,
    Trimestre,
    Periode,
    Interrogation,
    Examen,
    NoteTrimestrielle,
    NoteAnnuelle,
    Message,
    Notification,
    EmploiDuTemps,
)
from .serializers import (
    UserSerializer,
    EleveSerializer,
    ClasseSerializer,
    MatiereSerializer,
    DevoirSerializer,
    AnneeScolaireSerializer,
    TrimestreSerializer,
    PeriodeSerializer,
    InterrogationSerializer,
    ExamenSerializer,
    NoteTrimestrielleSerializer,
    NoteAnnuelleSerializer,
    MessageSerializer,
    NotificationSerializer,
    EmploiDuTempsSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)
from .services import (
    NoteService,
    PromotionService,
    NotificationService,
    AuthTokenService,
)

try:
    from .permissions import (
        IsDeveloppeur,
        IsAdmin,
        IsProfesseur,
        IsParent,
        CanManageUsers,
        CanManageEleves,
        CanManageNotes,
    )
except ImportError:
    IsDeveloppeur = IsAuthenticated
    IsAdmin = IsAuthenticated
    IsProfesseur = IsAuthenticated
    IsParent = IsAuthenticated
    CanManageUsers = IsAuthenticated
    CanManageEleves = IsAuthenticated
    CanManageNotes = IsAuthenticated

# ============ VUES D'AUTHENTIFICATION ============


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """Inscription d'un nouvel utilisateur"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = AuthTokenService.create_token(user)
        return Response(
            {
                "message": "Utilisateur créé avec succès",
                "user": {
                    "id": str(user.id),
                    "nom": user.nom,
                    "prenom": user.prenom,
                    "email": user.email,
                    "role": user.role,
                },
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """Connexion d'un utilisateur"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        token = AuthTokenService.create_token(user)

        return Response(
            {
                "message": "Connexion réussie",
                "user": {
                    "id": str(user.id),
                    "nom": user.nom,
                    "prenom": user.prenom,
                    "email": user.email,
                    "role": user.role,
                    "telephone": user.telephone,
                },
                "token": token.key,
            },
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """Déconnexion d'un utilisateur"""
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if auth_header.startswith("Token "):
        token_key = auth_header.split(" ")[1]
        if AuthTokenService.delete_token(token_key):
            return Response(
                {"message": "Déconnexion réussie"}, status=status.HTTP_200_OK
            )
    return Response(
        {"message": "Erreur lors de la déconnexion"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile(request):
    """Consultation et modification du profil utilisateur"""
    user = request.user
    if request.method == "GET":
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Profil mis à jour avec succès", "user": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Changement de mot de passe"""
    serializer = ChangePasswordSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Mot de passe modifié avec succès"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def token_info(request):
    """Informations sur le token actuel"""
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if auth_header.startswith("Bearer "):
        token_key = auth_header.split(" ")[1]
        from .models import AuthToken

        try:
            token = AuthToken.objects.get(key=token_key)
            return Response(
                {
                    "token_key": token.key[:10] + "...",
                    "created": token.created,
                    "user": {
                        "id": str(token.user.id),
                        "email": token.user.email,
                        "role": token.user.role,
                    },
                }
            )
        except AuthToken.DoesNotExist:
            return Response(
                {"error": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST
            )
    return Response({"error": "Aucun token fourni"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    """Actualiser le token"""
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if auth_header.startswith("Bearer "):
        old_token_key = auth_header.split(" ")[1]
        AuthTokenService.delete_token(old_token_key)
    new_token = AuthTokenService.create_token(request.user)
    return Response({"message": "Token actualisé avec succès", "token": new_token.key})


# ============ APIView DE BASE POUR CRUD ============


class BaseMongoAPIView(APIView):
    """Classe de base pour tous les APIView MongoDB"""

    permission_classes = [IsAuthenticated]
    serializer_class = None
    model_class = None

    def get(self, request, pk=None):
        """Récupérer un ou plusieurs objets"""
        if pk:
            try:
                obj = self.model_class.objects.get(id=pk)
                serializer = self.serializer_class(obj)
                return Response(serializer.data)
            except self.model_class.DoesNotExist:
                return Response(
                    {"error": "Objet non trouvé"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            objects = self.model_class.objects.all()
            serializer = self.serializer_class([obj for obj in objects], many=True)
            return Response(serializer.data)

    def post(self, request):
        """Créer un nouvel objet"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Mettre à jour complètement un objet"""
        try:
            obj = self.model_class.objects.get(id=pk)
            serializer = self.serializer_class(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except self.model_class.DoesNotExist:
            return Response(
                {"error": "Objet non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, pk):
        """Mettre à jour partiellement un objet"""
        try:
            obj = self.model_class.objects.get(id=pk)
            serializer = self.serializer_class(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except self.model_class.DoesNotExist:
            return Response(
                {"error": "Objet non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        """Supprimer un objet"""
        try:
            obj = self.model_class.objects.get(id=pk)
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except self.model_class.DoesNotExist:
            return Response(
                {"error": "Objet non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )


# ============ APIView POUR CHAQUE MODÈLE ============


class UserAPIView(BaseMongoAPIView):
    serializer_class = UserSerializer
    model_class = User


class EleveAPIView(BaseMongoAPIView):
    serializer_class = EleveSerializer
    model_class = Eleve


class ClasseAPIView(BaseMongoAPIView):
    serializer_class = ClasseSerializer
    model_class = Classe


class MatiereAPIView(BaseMongoAPIView):
    serializer_class = MatiereSerializer
    model_class = Matiere


class DevoirAPIView(BaseMongoAPIView):
    serializer_class = DevoirSerializer
    model_class = Devoir

    def post(self, request):
        """Créer un devoir avec notifications"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            devoir = serializer.save()
            # Créer des notifications pour les parents
            NotificationService.creer_notification_devoir(str(devoir.id))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnneeScolaireAPIView(BaseMongoAPIView):
    serializer_class = AnneeScolaireSerializer
    model_class = AnneeScolaire


class TrimestreAPIView(BaseMongoAPIView):
    serializer_class = TrimestreSerializer
    model_class = Trimestre


class PeriodeAPIView(BaseMongoAPIView):
    serializer_class = PeriodeSerializer
    model_class = Periode


class InterrogationAPIView(BaseMongoAPIView):
    serializer_class = InterrogationSerializer
    model_class = Interrogation


class ExamenAPIView(BaseMongoAPIView):
    serializer_class = ExamenSerializer
    model_class = Examen


class NoteTrimestrielleAPIView(BaseMongoAPIView):
    serializer_class = NoteTrimestrielleSerializer
    model_class = NoteTrimestrielle


class NoteAnnuelleAPIView(BaseMongoAPIView):
    serializer_class = NoteAnnuelleSerializer
    model_class = NoteAnnuelle


class MessageAPIView(BaseMongoAPIView):
    serializer_class = MessageSerializer
    model_class = Message

    def post(self, request):
        """Créer un message avec notification"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            message = serializer.save()
            # Créer une notification pour le destinataire
            NotificationService.creer_notification_message(str(message.id))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationAPIView(BaseMongoAPIView):
    serializer_class = NotificationSerializer
    model_class = Notification

    def get(self, request, pk=None):
        """Récupérer uniquement les notifications de l'utilisateur connecté"""
        if pk:
            try:
                notification = Notification.objects.get(
                    id=pk, destinataire=request.user
                )
                serializer = self.serializer_class(notification)
                return Response(serializer.data)
            except Notification.DoesNotExist:
                return Response(
                    {"error": "Notification non trouvée"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            notifications = Notification.objects.filter(destinataire=request.user)
            serializer = self.serializer_class(
                [notif for notif in notifications], many=True
            )
            return Response(serializer.data)


class EmploiDuTempsAPIView(BaseMongoAPIView):
    serializer_class = EmploiDuTempsSerializer
    model_class = EmploiDuTemps


# ============ APIView POUR OPÉRATIONS COMPLEXES ============


class CalculNotesTrimestriellesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Calcul automatique des notes trimestrielles"""
        if not (request.user.role in ["admin", "developpeur", "professeur"]):
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        trimestre_id = request.data.get("trimestre_id")
        if not trimestre_id:
            return Response(
                {"error": "trimestre_id required"}, status=status.HTTP_400_BAD_REQUEST
            )

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
                            "noteFinale": resultat["note_finale"],
                            "details": {
                                "moyenneTravaux": resultat["moyenne_travaux"],
                                "noteExamen": resultat["note_examen"],
                            },
                        },
                    )

                    if not created:
                        note_trim.noteFinale = resultat["note_finale"]
                        note_trim.save()

                    notes_calculees += 1

            return Response({"message": f"{notes_calculees} notes calculées"})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PromotionAutomatiqueAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Promotion automatique des élèves"""
        if not (request.user.role in ["admin", "developpeur"]):
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        annee_id = request.data.get("annee_scolaire_id")
        methode_subdivision = request.data.get("methode_subdivision", "auto")

        if not annee_id:
            return Response(
                {"error": "annee_scolaire_id required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            eleves = Eleve.objects.all()
            promotions_reussies = 0
            promotions_echouees = 0

            for eleve in eleves:
                resultat = PromotionService.promouvoir_eleve(
                    str(eleve.id), annee_id, methode_subdivision
                )

                if resultat["promotion_effectuee"]:
                    promotions_reussies += 1
                else:
                    promotions_echouees += 1

            return Response(
                {
                    "message": "Promotion automatique terminée",
                    "promotions_reussies": promotions_reussies,
                    "promotions_echouees": promotions_echouees,
                }
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AffecterParentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Affecter un ou plusieurs élèves à un parent"""
        if not (request.user.role in ["admin", "developpeur", "professeur"]):
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        parent_id = request.data.get("parent_id")
        eleve_ids = request.data.get("eleve_ids", [])

        if not parent_id or not eleve_ids:
            return Response(
                {"error": "parent_id and eleve_ids required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            parent = User.objects.get(id=parent_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND
            )

        assigned = []
        errors = []

        for eleve_id in eleve_ids:
            try:
                eleve = Eleve.objects.get(id=eleve_id)

                # Ajouter le parent à l'élève si pas déjà présent
                parent_ids = [str(p.id) for p in eleve.parents]
                if str(parent.id) not in parent_ids:
                    eleve.parents.append(parent)
                    eleve.save()

                # Ajouter l'élève au parent si pas déjà présent
                eleve_ids_parent = [str(e.id) for e in parent.enfants]
                if str(eleve.id) not in eleve_ids_parent:
                    parent.enfants.append(eleve)
                    parent.save()

                assigned.append(
                    {
                        "eleve_id": str(eleve.id),
                        "eleve_nom": f"{eleve.prenom} {eleve.nom}",
                    }
                )

            except Eleve.DoesNotExist:
                errors.append({"eleve_id": eleve_id, "error": "Eleve not found"})

        response_data = {
            "message": f"Affecté {len(assigned)} élève(s) au parent {parent.prenom} {parent.nom}",
            "assigned": assigned,
        }

        if errors:
            response_data["errors"] = errors

        return Response(response_data)


class GestionNotificationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Marquer toutes les notifications comme lues"""
        result = NotificationService.marquer_notifications_lues(str(request.user.id))
        return Response(result)

    def patch(self, request, pk):
        """Marquer une notification spécifique comme lue"""
        try:
            notification = Notification.objects.get(id=pk, destinataire=request.user)
            notification.lu = True
            notification.save()
            return Response({"status": "notification marquée comme lue"})
        except Notification.DoesNotExist:
            return Response(
                {"error": "Notification introuvable"}, status=status.HTTP_404_NOT_FOUND
            )


class AffecterProfesseurAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Affecter des matières et/ou des classes à un professeur"""
        if not (request.user.role in ["admin", "developpeur", "professeur"]):
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        professeur_id = request.data.get("professeur_id")
        matiere_ids = request.data.get("matiere_ids", [])
        classe_ids = request.data.get("classe_ids", [])

        if not professeur_id:
            return Response(
                {"error": "professeur_id required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not matiere_ids and not classe_ids:
            return Response(
                {"error": "matiere_ids or classe_ids required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            professeur = User.objects.get(id=professeur_id, role="professeur")
        except User.DoesNotExist:
            return Response(
                {"error": "Professeur not found or not a professeur"}, status=status.HTTP_404_NOT_FOUND
            )

        assigned_matieres = []
        assigned_classes = []

        # Affecter les matières directement
        for matiere_id in matiere_ids:
            try:
                matiere = Matiere.objects.get(id=matiere_id)
                matiere.professeur = professeur
                matiere.save()
                assigned_matieres.append({
                    "matiere_id": str(matiere.id),
                    "matiere_nom": matiere.nom,
                })
            except Matiere.DoesNotExist:
                pass  # Ignore silently or collect errors

        # Affecter toutes les matières des classes spécifiées
        for classe_id in classe_ids:
            try:
                classe = Classe.objects.get(id=classe_id)
                matieres_classe = Matiere.objects.filter(classe=classe)
                for matiere in matieres_classe:
                    matiere.professeur = professeur
                    matiere.save()
                    assigned_matieres.append({
                        "matiere_id": str(matiere.id),
                        "matiere_nom": matiere.nom,
                        "classe_nom": classe.nom,
                    })
                assigned_classes.append({
                    "classe_id": str(classe.id),
                    "classe_nom": classe.nom,
                })
            except Classe.DoesNotExist:
                pass  # Ignore silently

        response_data = {
            "message": f"Affecté {len(assigned_matieres)} matière(s) au professeur {professeur.prenom} {professeur.nom}",
            "assigned_matieres": assigned_matieres,
            "assigned_classes": assigned_classes,
        }

        return Response(response_data)
