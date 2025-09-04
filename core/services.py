"""
Services pour la logique métier complexe du système de gestion scolaire
"""
from datetime import datetime
import random
from typing import List, Dict, Any

from .models import (
    User, Eleve, Classe, Matiere, Devoir, AnneeScolaire, 
    Trimestre, Periode, Interrogation, Examen, NoteTrimestrielle, 
    NoteAnnuelle, Message, Notification, EmploiDuTemps,
    DetailsNoteTrimestrielle, DetailNoteAnnuelle
)

class NoteService:
    """Service pour le calcul des notes"""
    
    @staticmethod
    def calculer_moyenne_travaux(eleve_id: str, matiere_id: str, periode_id: str) -> float:
        """Calcule la moyenne des travaux (interrogations) pour un élève dans une matière sur une période"""
        interrogations = Interrogation.objects.filter(
            eleve=eleve_id,
            matiere=matiere_id,
            periode=periode_id
        )
        
        if not interrogations:
            return 0.0
            
        total = sum([interro.note for interro in interrogations if interro.note is not None])
        count = len([interro for interro in interrogations if interro.note is not None])
        
        return total / count if count > 0 else 0.0

    @staticmethod
    def get_note_examen(eleve_id: str, matiere_id: str, trimestre_id: str) -> float:
        """Récupère la note d'examen pour un élève dans une matière sur un trimestre"""
        examen = Examen.objects.filter(
            eleve=eleve_id,
            matiere=matiere_id,
            trimestre=trimestre_id
        ).first()
        
        return examen.note if examen and examen.note is not None else 0.0

    @staticmethod
    def calculer_note_trimestrielle(eleve_id: str, matiere_id: str, trimestre_id: str) -> Dict[str, float]:
        """Calcule la note trimestrielle : 50% travaux + 50% examen"""
        trimestre = Trimestre.objects.get(id=trimestre_id)
        periodes = trimestre.periodes
        
        # Calculer la moyenne des travaux sur toutes les périodes du trimestre
        moyennes_periodes = []
        for periode in periodes:
            moyenne_periode = NoteService.calculer_moyenne_travaux(eleve_id, matiere_id, str(periode.id))
            if moyenne_periode > 0:
                moyennes_periodes.append(moyenne_periode)
        
        moyenne_travaux = sum(moyennes_periodes) / len(moyennes_periodes) if moyennes_periodes else 0.0
        
        # Récupérer la note d'examen
        note_examen = NoteService.get_note_examen(eleve_id, matiere_id, trimestre_id)
        
        # Calcul final : 50% travaux + 50% examen
        note_finale = (moyenne_travaux * 0.5) + (note_examen * 0.5)
        
        return {
            'note_finale': note_finale,
            'moyenne_travaux': moyenne_travaux,
            'note_examen': note_examen
        }

    @staticmethod
    def calculer_note_annuelle(eleve_id: str, matiere_id: str, annee_scolaire_id: str) -> Dict[str, Any]:
        """Calcule la note annuelle : moyenne des 3 trimestres"""
        annee = AnneeScolaire.objects.get(id=annee_scolaire_id)
        trimestres = annee.trimestres
        
        notes_trimestres = []
        details_trimestres = []
        
        for trimestre in trimestres:
            note_trim = NoteTrimestrielle.objects.filter(
                eleve=eleve_id,
                matiere=matiere_id,
                trimestre=str(trimestre.id)
            ).first()
            
            if note_trim and note_trim.noteFinale is not None:
                notes_trimestres.append(note_trim.noteFinale)
                details_trimestres.append({
                    'trimestre': str(trimestre.id),
                    'note_trimestre': note_trim.noteFinale
                })
        
        note_annuelle = sum(notes_trimestres) / len(notes_trimestres) if notes_trimestres else 0.0
        
        return {
            'note_finale': note_annuelle,
            'details': details_trimestres,
            'nb_trimestres': len(notes_trimestres)
        }

class PromotionService:
    """Service pour la promotion automatique des élèves"""
    
    @staticmethod
    def evaluer_promotion(eleve_id: str, annee_scolaire_id: str) -> Dict[str, Any]:
        """Évalue si un élève peut être promu automatiquement"""
        eleve = Eleve.objects.get(id=eleve_id)
        classe_actuelle = eleve.classe
        
        if not classe_actuelle:
            return {'peut_etre_promu': False, 'raison': 'Pas de classe assignée'}
        
        # Récupérer toutes les matières de la classe
        matieres = Matiere.objects.filter(classe=classe_actuelle)
        
        notes_annuelles = []
        for matiere in matieres:
            note_annuelle_obj = NoteAnnuelle.objects.filter(
                eleve=eleve_id,
                matiere=str(matiere.id),
                anneeScolaire=annee_scolaire_id
            ).first()
            
            if note_annuelle_obj and note_annuelle_obj.noteFinale is not None:
                notes_annuelles.append(note_annuelle_obj.noteFinale)
        
        if not notes_annuelles:
            return {'peut_etre_promu': False, 'raison': 'Aucune note disponible'}
        
        # Calculer la moyenne générale
        moyenne_generale = sum(notes_annuelles) / len(notes_annuelles)
        
        # Vérifier le seuil de promotion
        peut_etre_promu = moyenne_generale >= classe_actuelle.seuilPromotion
        
        return {
            'peut_etre_promu': peut_etre_promu,
            'moyenne_generale': moyenne_generale,
            'seuil_requis': classe_actuelle.seuilPromotion,
            'nb_matieres': len(notes_annuelles)
        }
    
    @staticmethod
    def promouvoir_eleve(eleve_id: str, annee_scolaire_id: str, methode_subdivision: str = 'auto') -> Dict[str, Any]:
        """Promouvoir un élève à la classe suivante"""
        eleve = Eleve.objects.get(id=eleve_id)
        evaluation = PromotionService.evaluer_promotion(eleve_id, annee_scolaire_id)
        
        if not evaluation['peut_etre_promu']:
            return {
                'promotion_effectuee': False, 
                'raison': f"Moyenne insuffisante: {evaluation.get('moyenne_generale', 0):.2f}/{evaluation.get('seuil_requis', 0)}"
            }
        
        # Trouver la classe suivante
        classe_actuelle = eleve.classe
        niveau_suivant = classe_actuelle.niveau + 1
        
        classe_suivante = Classe.objects.filter(
            niveau=niveau_suivant,
            typeClasse=classe_actuelle.typeClasse
        ).first()
        
        if not classe_suivante:
            return {'promotion_effectuee': False, 'raison': 'Aucune classe suivante trouvée'}
        
        # Choisir la subdivision
        if methode_subdivision == 'auto' and classe_suivante.subdivisions:
            subdivision_choisie = random.choice([sub.nom for sub in classe_suivante.subdivisions])
        else:
            subdivision_choisie = classe_suivante.subdivisions[0].nom if classe_suivante.subdivisions else 'A'
        
        # Mettre à jour la note annuelle avec les infos de promotion
        for matiere in Matiere.objects.filter(classe=classe_actuelle):
            note_annuelle = NoteAnnuelle.objects.filter(
                eleve=eleve_id,
                matiere=str(matiere.id),
                anneeScolaire=annee_scolaire_id
            ).first()
            
            if note_annuelle:
                note_annuelle.promotionAutomatique = True
                note_annuelle.nouvelleClasse = classe_suivante
                note_annuelle.nouvelleSubdivision = subdivision_choisie
                note_annuelle.save()
        
        return {
            'promotion_effectuee': True,
            'nouvelle_classe': classe_suivante.nom,
            'nouvelle_subdivision': subdivision_choisie,
            'moyenne_generale': evaluation['moyenne_generale']
        }

class NotificationService:
    """Service pour la gestion des notifications automatiques"""
    
    @staticmethod
    def creer_notification_devoir(devoir_id: str):
        """Crée des notifications pour un nouveau devoir"""
        devoir = Devoir.objects.get(id=devoir_id)
        
        # Récupérer tous les élèves de la classe/subdivision concernée
        eleves = Eleve.objects.filter(
            classe=devoir.classe,
            subdivision=devoir.subdivision
        )
        
        notifications_creees = 0
        for eleve in eleves:
            # Notifier les parents de chaque élève
            for parent in eleve.parents:
                notification = Notification(
                    destinataire=parent,
                    type='devoir',
                    referenceId=devoir_id,
                    dateEnvoi=datetime.utcnow(),
                    lu=False
                )
                notification.save()
                notifications_creees += 1
        
        return {'notifications_creees': notifications_creees}
    
    @staticmethod
    def creer_notification_message(message_id: str):
        """Crée une notification pour un nouveau message"""
        message = Message.objects.get(id=message_id)
        
        notification = Notification(
            destinataire=message.receiver,
            type='message',
            referenceId=message_id,
            dateEnvoi=datetime.utcnow(),
            lu=False
        )
        notification.save()
        
        return {'notification_creee': True}
    
    @staticmethod
    def marquer_notifications_lues(user_id: str, type_notification: str = None):
        """Marque toutes les notifications d'un utilisateur comme lues"""
        query = {'destinataire': user_id}
        if type_notification:
            query['type'] = type_notification
        
        notifications = Notification.objects.filter(**query)
        count = 0
        for notif in notifications:
            if not notif.lu:
                notif.lu = True
                notif.save()
                count += 1
        
        return {'notifications_marquees': count}

class AuthTokenService:
    """Service pour la gestion des tokens d'authentification"""
    
    @staticmethod
    def create_token(user):
        """Crée un token pour un utilisateur"""
        from .models import AuthToken
        
        # Supprimer les anciens tokens de cet utilisateur (optionnel)
        AuthToken.objects.filter(user=user).delete()
        
        # Créer un nouveau token
        token = AuthToken(user=user)
        token.save()
        
        return token
    
    @staticmethod
    def get_user_by_token(token_key):
        """Récupère un utilisateur par sa clé de token"""
        from .models import AuthToken
        
        try:
            token = AuthToken.objects.get(key=token_key)
            return token.user
        except AuthToken.DoesNotExist:
            return None
    
    @staticmethod
    def delete_token(token_key):
        """Supprime un token"""
        from .models import AuthToken
        
        try:
            token = AuthToken.objects.get(key=token_key)
            token.delete()
            return True
        except AuthToken.DoesNotExist:
            return False
    
    @staticmethod
    def validate_token(token_key):
        """Valide un token et retourne l'utilisateur associé"""
        user = AuthTokenService.get_user_by_token(token_key)
        return user is not None, user
    
    @staticmethod
    def cleanup_expired_tokens(days_old=30):
        """Nettoie les tokens expirés (optionnel)"""
        from .models import AuthToken
        from datetime import timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        expired_tokens = AuthToken.objects.filter(created__lt=cutoff_date)
        count = len(expired_tokens)
        expired_tokens.delete()
        
        return {'tokens_supprimes': count}
        return total / len(interrogations)
    
    @staticmethod
    def calculer_note_trimestrielle(eleve_id: str, matiere_id: str, trimestre_id: str) -> Dict[str, Any]:
        """
        Calcule la note trimestrielle : 50% moyenne travaux + 50% note examen
        """
        # Récupérer les périodes du trimestre
        trimestre = Trimestre.objects.get(id=trimestre_id)
        periodes = trimestre.periodes
        
        # Calculer la moyenne des travaux sur toutes les périodes du trimestre
        moyennes_travaux = []
        for periode in periodes:
            moyenne = NoteService.calculer_moyenne_travaux(eleve_id, matiere_id, str(periode.id))
            if moyenne > 0:
                moyennes_travaux.append(moyenne)
        
        moyenne_travaux_totale = sum(moyennes_travaux) / len(moyennes_travaux) if moyennes_travaux else 0
        
        # Récupérer la note d'examen
        examen = Examen.objects.filter(
            eleve=eleve_id,
            matiere=matiere_id,
            trimestre=trimestre_id
        ).first()
        
        note_examen = examen.note if examen and examen.note else 0
        
        # Calcul final : 50% travaux + 50% examen
        note_finale = (moyenne_travaux_totale * 0.5) + (note_examen * 0.5)
        
        return {
            'note_finale': note_finale,
            'moyenne_travaux': moyenne_travaux_totale,
            'note_examen': note_examen
        }
    
    @staticmethod
    def calculer_note_annuelle(eleve_id: str, matiere_id: str, annee_scolaire_id: str) -> Dict[str, Any]:
        """
        Calcule la note annuelle : moyenne des 3 notes trimestrielles
        """
        annee = AnneeScolaire.objects.get(id=annee_scolaire_id)
        trimestres = annee.trimestres
        
        notes_trimestrielles = []
        details_trimestres = []
        
        for trimestre in trimestres:
            note_trim = NoteTrimestrielle.objects.filter(
                eleve=eleve_id,
                matiere=matiere_id,
                trimestre=str(trimestre.id)
            ).first()
            
            if note_trim and note_trim.noteFinale:
                notes_trimestrielles.append(note_trim.noteFinale)
                details_trimestres.append({
                    'trimestre': str(trimestre.id),
                    'note_trimestre': note_trim.noteFinale
                })
        
        note_annuelle = sum(notes_trimestrielles) / len(notes_trimestrielles) if notes_trimestrielles else 0
        
        return {
            'note_finale': note_annuelle,
            'details': details_trimestres
        }

class PromotionService:
    """Service pour la promotion automatique des élèves"""
    
    @staticmethod
    def evaluer_promotion_eleve(eleve_id: str, annee_scolaire_id: str) -> Dict[str, Any]:
        """
        Évalue si un élève peut être promu automatiquement
        """
        eleve = Eleve.objects.get(id=eleve_id)
        classe = eleve.classe
        
        # Récupérer toutes les notes annuelles de l'élève
        notes_annuelles = NoteAnnuelle.objects.filter(
            eleve=eleve_id,
            anneeScolaire=annee_scolaire_id
        )
        
        # Calculer la moyenne générale pondérée
        total_points = 0
        total_coefficients = 0
        
        for note in notes_annuelles:
            matiere = note.matiere
            coefficient = matiere.coefficient or 1
            
            total_points += note.noteFinale * coefficient
            total_coefficients += coefficient
        
        moyenne_generale = total_points / total_coefficients if total_coefficients > 0 else 0
        
        # Vérifier si l'élève atteint le seuil de promotion
        seuil = classe.seuilPromotion or 10  # Seuil par défaut : 10/20
        promotion_automatique = moyenne_generale >= seuil
        
        return {
            'moyenne_generale': moyenne_generale,
            'seuil_promotion': seuil,
            'promotion_automatique': promotion_automatique,
            'nouvelle_classe': None,  # À déterminer selon la logique métier
            'nouvelle_subdivision': None
        }
    
    @staticmethod
    def promouvoir_eleves_classe(classe_id: str, annee_scolaire_id: str, methode_subdivision: str = 'auto') -> Dict[str, Any]:
        """
        Promouvoir tous les élèves éligibles d'une classe
        """
        eleves = Eleve.objects.filter(classe=classe_id)
        resultats = {
            'promus': [],
            'non_promus': [],
            'total': len(eleves)
        }
        
        for eleve in eleves:
            evaluation = PromotionService.evaluer_promotion_eleve(str(eleve.id), annee_scolaire_id)
            
            if evaluation['promotion_automatique']:
                # Logique pour déterminer la nouvelle classe
                # (dépend de la structure des classes dans le système)
                resultats['promus'].append({
                    'eleve_id': str(eleve.id),
                    'nom_complet': f"{eleve.prenom} {eleve.nom}",
                    'moyenne': evaluation['moyenne_generale']
                })
            else:
                resultats['non_promus'].append({
                    'eleve_id': str(eleve.id),
                    'nom_complet': f"{eleve.prenom} {eleve.nom}",
                    'moyenne': evaluation['moyenne_generale']
                })
        
        return resultats

class NotificationService:
    """Service pour la gestion des notifications"""
    
    @staticmethod
    def creer_notification(destinataire_id: str, type_notif: str, reference_id: str):
        """
        Crée une nouvelle notification
        """
        notification = Notification(
            destinataire=destinataire_id,
            type=type_notif,
            referenceId=reference_id,
            lu=False,
            dateEnvoi=datetime.utcnow()
        )
        notification.save()
        return notification
    
    @staticmethod
    def notifier_nouveau_devoir(devoir_id: str):
        """
        Notifie les parents et élèves d'un nouveau devoir
        """
        devoir = Devoir.objects.get(id=devoir_id)
        
        # Trouver tous les élèves de la classe/subdivision concernée
        eleves = Eleve.objects.filter(
            classe=devoir.classe,
            subdivision=devoir.subdivision
        )
        
        notifications_creees = []
        
        for eleve in eleves:
            # Notifier les parents
            for parent in eleve.parents:
                notif = NotificationService.creer_notification(
                    str(parent.id),
                    'devoir',
                    devoir_id
                )
                notifications_creees.append(notif)
        
        return notifications_creees
    
    @staticmethod
    def notifier_nouveau_message(message_id: str):
        """
        Notifie le destinataire d'un nouveau message
        """
        message = Message.objects.get(id=message_id)
        
        notification = NotificationService.creer_notification(
            str(message.receiver.id),
            'message',
            message_id
        )
        
        return notification

class SubdivisionService:
    """Service pour la gestion des subdivisions"""
    
    @staticmethod
    def affecter_subdivision_automatique(eleves_ids: List[str], classe_id: str):
        """
        Affecte automatiquement et aléatoirement les élèves aux subdivisions
        """
        classe = Classe.objects.get(id=classe_id)
        subdivisions_noms = [sub.nom for sub in classe.subdivisions]
        
        if not subdivisions_noms:
            raise ValueError("Aucune subdivision définie pour cette classe")
        
        resultats = []
        
        for eleve_id in eleves_ids:
            eleve = Eleve.objects.get(id=eleve_id)
            subdivision_choisie = random.choice(subdivisions_noms)
            
            eleve.subdivision = subdivision_choisie
            eleve.methodeSubdivision = 'auto'
            eleve.save()
            
            resultats.append({
                'eleve_id': eleve_id,
                'nom_complet': f"{eleve.prenom} {eleve.nom}",
                'subdivision': subdivision_choisie
            })
        
        return resultats
    
    @staticmethod
    def affecter_subdivision_manuelle(affectations: List[Dict[str, str]]):
        """
        Affecte manuellement les élèves aux subdivisions
        affectations: [{'eleve_id': 'xxx', 'subdivision': 'A'}, ...]
        """
        resultats = []
        
        for affectation in affectations:
            eleve = Eleve.objects.get(id=affectation['eleve_id'])
            eleve.subdivision = affectation['subdivision']
            eleve.methodeSubdivision = 'manuel'
            eleve.save()
            
            resultats.append({
                'eleve_id': affectation['eleve_id'],
                'nom_complet': f"{eleve.prenom} {eleve.nom}",
                'subdivision': affectation['subdivision']
            })
        
        return resultats
