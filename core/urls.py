from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router pour les API ViewSets
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'eleves', views.EleveViewSet)
router.register(r'classes', views.ClasseViewSet)
router.register(r'matieres', views.MatiereViewSet)
router.register(r'devoirs', views.DevoirViewSet)
router.register(r'annees-scolaires', views.AnneeScolaireViewSet)
router.register(r'trimestres', views.TrimestreViewSet)
router.register(r'periodes', views.PeriodeViewSet)
router.register(r'interrogations', views.InterrogationViewSet)
router.register(r'examens', views.ExamenViewSet)
router.register(r'notes-trimestrielles', views.NoteTrimestrielleViewSet)
router.register(r'notes-annuelles', views.NoteAnnuelleViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'emplois-du-temps', views.EmploiDuTempsViewSet)

urlpatterns = [
    # Routes d'authentification
    path('api/auth/register/', views.register, name='register'),
    path('api/auth/login/', views.login, name='login'),
    path('api/auth/logout/', views.logout, name='logout'),
    path('api/auth/profile/', views.profile, name='profile'),
    path('api/auth/change-password/', views.change_password, name='change_password'),
    path('api/auth/token-info/', views.token_info, name='token_info'),
    path('api/auth/refresh-token/', views.refresh_token, name='refresh_token'),
    
    # Routes API REST
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
