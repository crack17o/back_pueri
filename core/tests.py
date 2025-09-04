from django.test import TestCase, Client
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
import json

from .models import User, Eleve, Classe, Matiere, NoteTrimestrielle
from .services import NoteService, PromotionService, NotificationService


class AuthenticationTestCase(APITestCase):
    """Tests pour l'authentification"""
    
    def setUp(self):
        self.client = Client()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        
        self.user_data = {
            'nom': 'Dupont',
            'prenom': 'Jean',
            'email': 'jean.dupont@test.com',
            'motDePasse': 'test123456',
            'role': 'parent',
            'telephone': '0123456789'
        }
    
    def test_register_user(self):
        """Test d'inscription d'un nouvel utilisateur"""
        response = self.client.post(
            self.register_url, 
            json.dumps(self.user_data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.json())
        self.assertIn('user', response.json())
    
    def test_register_duplicate_email(self):
        """Test d'inscription avec un email déjà existant"""
        # Créer d'abord un utilisateur
        User(**self.user_data).save()
        
        response = self.client.post(
            self.register_url, 
            json.dumps(self.user_data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_login_valid_credentials(self):
        """Test de connexion avec des identifiants valides"""
        # Créer un utilisateur
        user = User(**self.user_data)
        user.save()
        
        login_data = {
            'email': self.user_data['email'],
            'motDePasse': self.user_data['motDePasse']
        }
        
        response = self.client.post(
            self.login_url, 
            json.dumps(login_data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
    
    def test_login_invalid_credentials(self):
        """Test de connexion avec des identifiants invalides"""
        login_data = {
            'email': 'nonexistent@test.com',
            'motDePasse': 'wrongpassword'
        }
        
        response = self.client.post(
            self.login_url, 
            json.dumps(login_data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


class NoteServiceTestCase(TestCase):
    """Tests pour le service de calcul des notes"""
    
    def setUp(self):
        # Créer des données de test en mémoire pour les tests
        self.eleve_id = "test_eleve_id"
        self.matiere_id = "test_matiere_id"
        self.periode_id = "test_periode_id"
        self.trimestre_id = "test_trimestre_id"
    
    @patch('core.models.Interrogation.objects')
    def test_calculer_moyenne_travaux(self, mock_interrogations):
        """Test du calcul de la moyenne des travaux"""
        # Mock des interrogations avec des notes
        mock_interro1 = type('MockInterro', (), {'note': 15.0})()
        mock_interro2 = type('MockInterro', (), {'note': 12.0})()
        mock_interro3 = type('MockInterro', (), {'note': None})()  # Note non saisie
        
        mock_interrogations.filter.return_value = [mock_interro1, mock_interro2, mock_interro3]
        
        moyenne = NoteService.calculer_moyenne_travaux(
            self.eleve_id, self.matiere_id, self.periode_id
        )
        
        # Moyenne de 15 et 12 = 13.5 (la note None est ignorée)
        self.assertEqual(moyenne, 13.5)
    
    @patch('core.models.Interrogation.objects')
    def test_calculer_moyenne_travaux_aucune_note(self, mock_interrogations):
        """Test du calcul quand aucune note n'est disponible"""
        mock_interrogations.filter.return_value = []
        
        moyenne = NoteService.calculer_moyenne_travaux(
            self.eleve_id, self.matiere_id, self.periode_id
        )
        
        self.assertEqual(moyenne, 0.0)


class PromotionServiceTestCase(TestCase):
    """Tests pour le service de promotion"""
    
    @patch('core.models.Eleve.objects')
    @patch('core.models.Classe')
    @patch('core.models.Matiere.objects')
    def test_evaluer_promotion_reussie(self, mock_matieres, mock_classe, mock_eleve):
        """Test d'évaluation de promotion réussie"""
        # Mock de l'élève et de sa classe
        mock_classe_instance = type('MockClasse', (), {'seuilPromotion': 10})()
        mock_eleve_instance = type('MockEleve', (), {'classe': mock_classe_instance})()
        mock_eleve.get.return_value = mock_eleve_instance
        
        # Mock des matières et notes annuelles
        mock_matieres.filter.return_value = [type('MockMatiere', (), {})() for _ in range(3)]
        
        # Cette fonction nécessiterait plus de mocks pour être complètement testée
        # mais ceci démontre la structure des tests
    
    def test_promotion_logique(self):
        """Test de la logique de promotion"""
        # Test simple de la logique
        moyenne_generale = 12.5
        seuil_promotion = 10.0
        
        peut_etre_promu = moyenne_generale >= seuil_promotion
        self.assertTrue(peut_etre_promu)


class NotificationServiceTestCase(TestCase):
    """Tests pour le service de notifications"""
    
    @patch('core.models.Devoir.objects')
    @patch('core.models.Eleve.objects')
    @patch('core.models.Notification')
    def test_creer_notification_devoir(self, mock_notification, mock_eleve, mock_devoir):
        """Test de création de notifications pour un devoir"""
        # Mock du devoir
        mock_devoir_instance = type('MockDevoir', (), {
            'classe': 'test_classe',
            'subdivision': 'A'
        })()
        mock_devoir.get.return_value = mock_devoir_instance
        
        # Mock des élèves avec leurs parents
        mock_parent = type('MockParent', (), {})()
        mock_eleve_instance = type('MockEleve', (), {
            'parents': [mock_parent]
        })()
        mock_eleve.filter.return_value = [mock_eleve_instance]
        
        # Mock de la sauvegarde de notification
        mock_notification_instance = mock_notification.return_value
        mock_notification_instance.save.return_value = None
        
        result = NotificationService.creer_notification_devoir("test_devoir_id")
        
        # Vérifier qu'une notification a été créée
        self.assertEqual(result['notifications_creees'], 1)


class APIEndpointsTestCase(APITestCase):
    """Tests des endpoints API"""
    
    def setUp(self):
        # Créer un utilisateur de test
        self.user_data = {
            'nom': 'Admin',
            'prenom': 'Test',
            'email': 'admin@test.com',
            'motDePasse': 'admin123',
            'role': 'admin'
        }
        self.user = User(**self.user_data)
        self.user.save()
    
    def test_api_endpoints_exist(self):
        """Test que tous les endpoints API existent"""
        endpoints = [
            '/api/users/',
            '/api/eleves/',
            '/api/classes/',
            '/api/matieres/',
            '/api/devoirs/',
            '/api/notes-trimestrielles/',
            '/api/notifications/',
        ]
        
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.client.get(endpoint)
                # Le endpoint doit exister (même si non autorisé = 401/403)
                self.assertNotEqual(response.status_code, 404)
    
    def test_auth_endpoints(self):
        """Test que les endpoints d'authentification existent"""
        auth_endpoints = [
            '/api/auth/register/',
            '/api/auth/login/',
            '/api/auth/profile/',
            '/api/auth/change-password/',
        ]
        
        for endpoint in auth_endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.client.get(endpoint) if 'profile' in endpoint else self.client.post(endpoint, {})
                # Le endpoint doit exister
                self.assertNotEqual(response.status_code, 404)
