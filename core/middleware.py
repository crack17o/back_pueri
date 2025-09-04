"""
Middleware personnalisé pour l'authentification avec MongoDB et mongoengine
"""
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from .services import AuthTokenService
import json

class MongoAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware pour l'authentification avec les utilisateurs MongoDB
    """
    
    def process_request(self, request):
        # Récupérer le token de l'en-tête Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if auth_header and auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]
            
            # Valider le token et récupérer l'utilisateur
            is_valid, user = AuthTokenService.validate_token(token_key)
            
            if is_valid and user:
                # Ajouter l'utilisateur à la requête
                request.user = user
                request.user.is_authenticated = True
            else:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

class AnonymousUser:
    """Utilisateur anonyme pour les requêtes non authentifiées"""
    is_authenticated = False
    role = None
    id = None
    email = None
    
    def __str__(self):
        return 'AnonymousUser'
    
    def __bool__(self):
        return False
