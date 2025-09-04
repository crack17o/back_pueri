from rest_framework.permissions import BasePermission

class IsDeveloppeur(BasePermission):
    """Permission pour les développeurs uniquement"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'developpeur'

class IsAdmin(BasePermission):
    """Permission pour les administrateurs"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'developpeur']

class IsProfesseur(BasePermission):
    """Permission pour les professeurs"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['professeur', 'admin', 'developpeur']

class IsParent(BasePermission):
    """Permission pour les parents"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['parent', 'admin', 'developpeur']

class CanManageUsers(BasePermission):
    """Gestion des utilisateurs - Admin et Développeur seulement"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Lecture pour tous les rôles authentifiés
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
            
        # Création/Modification/Suppression pour Admin et Développeur seulement
        return request.user.role in ['admin', 'developpeur']

class CanManageEleves(BasePermission):
    """Gestion des élèves selon le rôle"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.role
        
        # Développeur et Admin : tous les droits
        if user_role in ['admin', 'developpeur']:
            return True
            
        # Professeur : lecture seulement
        if user_role == 'professeur' and request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
            
        # Parent : lecture de ses enfants seulement
        if user_role == 'parent' and request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
            
        return False

class CanManageNotes(BasePermission):
    """Gestion des notes selon le rôle et les périodes actives"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.role
        
        # Développeur et Admin : tous les droits
        if user_role in ['admin', 'developpeur']:
            return True
            
        # Professeur : peut saisir/modifier pendant les périodes actives
        if user_role == 'professeur':
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                return True
            # TODO: Vérifier si la période est active pour les modifications
            return True
            
        # Parent : lecture seulement des notes de ses enfants
        if user_role == 'parent' and request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
            
        return False

class CanManageSchedule(BasePermission):
    """Gestion des emplois du temps"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.role
        
        # Développeur et Admin : tous les droits
        if user_role in ['admin', 'developpeur']:
            return True
            
        # Professeur et Parent : lecture seulement
        if user_role in ['professeur', 'parent'] and request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
            
        return False

class CanSendMessages(BasePermission):
    """Permission d'envoyer des messages selon le rôle"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Tous les rôles peuvent lire leurs messages
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
            
        # Professeurs et Parents peuvent envoyer des messages
        return request.user.role in ['professeur', 'parent', 'admin', 'developpeur']
