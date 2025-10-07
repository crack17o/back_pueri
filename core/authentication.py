from rest_framework import authentication, exceptions
from .models import AuthToken

class MongoTokenAuthentication(authentication.BaseAuthentication):
    """
    Authentification personnalisée pour les tokens MongoDB
    """
    keyword = 'Token'

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'En-tête de token invalide. Aucune informations d\'identification fournies.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'En-tête de token invalide. La chaîne de token ne doit pas contenir d\'espaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'En-tête de token invalide. Le token contient des caractères non valides.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            token = AuthToken.objects.get(key=key)
        except AuthToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Token non valide.')
        
        user = token.user
        
        # Vérifier que l'utilisateur est actif
        if not getattr(user, 'is_active', True):
            raise exceptions.AuthenticationDisabled('Utilisateur inactif.')
        
        return (user, token)

    def authenticate_header(self, request):
        return self.keyword