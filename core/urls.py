from django.urls import path, include
from . import views

urlpatterns = [
    # Authentification
    path('api/auth/register/', views.register, name='register'),
    path('api/auth/login/', views.login, name='login'),
    path('api/auth/logout/', views.logout, name='logout'),
    path('api/auth/profile/', views.profile, name='profile'),
    path('api/auth/change-password/', views.change_password, name='change_password'),
    path('api/auth/token-info/', views.token_info, name='token_info'),
    path('api/auth/refresh-token/', views.refresh_token, name='refresh_token'),
    
    # CRUD API
    path('api/users/', views.UserAPIView.as_view(), name='user-list'),
    path('api/users/<str:pk>/', views.UserAPIView.as_view(), name='user-detail'),
    
    path('api/eleves/', views.EleveAPIView.as_view(), name='eleve-list'),
    path('api/eleves/<str:pk>/', views.EleveAPIView.as_view(), name='eleve-detail'),
    
    path('api/classes/', views.ClasseAPIView.as_view(), name='classe-list'),
    path('api/classes/<str:pk>/', views.ClasseAPIView.as_view(), name='classe-detail'),
    
    path('api/matieres/', views.MatiereAPIView.as_view(), name='matiere-list'),
    path('api/matieres/<str:pk>/', views.MatiereAPIView.as_view(), name='matiere-detail'),
    
    path('api/devoirs/', views.DevoirAPIView.as_view(), name='devoir-list'),
    path('api/devoirs/<str:pk>/', views.DevoirAPIView.as_view(), name='devoir-detail'),
    
    path('api/annees-scolaires/', views.AnneeScolaireAPIView.as_view(), name='anneescolaire-list'),
    path('api/annees-scolaires/<str:pk>/', views.AnneeScolaireAPIView.as_view(), name='anneescolaire-detail'),
    
    path('api/trimestres/', views.TrimestreAPIView.as_view(), name='trimestre-list'),
    path('api/trimestres/<str:pk>/', views.TrimestreAPIView.as_view(), name='trimestre-detail'),
    
    path('api/periodes/', views.PeriodeAPIView.as_view(), name='periode-list'),
    path('api/periodes/<str:pk>/', views.PeriodeAPIView.as_view(), name='periode-detail'),
    
    path('api/interrogations/', views.InterrogationAPIView.as_view(), name='interrogation-list'),
    path('api/interrogations/<str:pk>/', views.InterrogationAPIView.as_view(), name='interrogation-detail'),
    
    path('api/examens/', views.ExamenAPIView.as_view(), name='examen-list'),
    path('api/examens/<str:pk>/', views.ExamenAPIView.as_view(), name='examen-detail'),
    
    path('api/notes-trimestrielles/', views.NoteTrimestrielleAPIView.as_view(), name='notetrimestrielle-list'),
    path('api/notes-trimestrielles/<str:pk>/', views.NoteTrimestrielleAPIView.as_view(), name='notetrimestrielle-detail'),
    
    path('api/notes-annuelles/', views.NoteAnnuelleAPIView.as_view(), name='noteannuelle-list'),
    path('api/notes-annuelles/<str:pk>/', views.NoteAnnuelleAPIView.as_view(), name='noteannuelle-detail'),
    
    path('api/messages/', views.MessageAPIView.as_view(), name='message-list'),
    path('api/messages/<str:pk>/', views.MessageAPIView.as_view(), name='message-detail'),
    
    path('api/notifications/', views.NotificationAPIView.as_view(), name='notification-list'),
    path('api/notifications/<str:pk>/', views.NotificationAPIView.as_view(), name='notification-detail'),
    
    path('api/emplois-du-temps/', views.EmploiDuTempsAPIView.as_view(), name='emploidutemps-list'),
    path('api/emplois-du-temps/<str:pk>/', views.EmploiDuTempsAPIView.as_view(), name='emploidutemps-detail'),
    
    # Opérations complexes
    path('api/calcul-notes-trimestrielles/', views.CalculNotesTrimestriellesAPIView.as_view(), name='calcul-notes'),
    path('api/promotion-automatique/', views.PromotionAutomatiqueAPIView.as_view(), name='promotion-auto'),
    path('api/affecter-parent/', views.AffecterParentAPIView.as_view(), name='affecter-parent'),
    path('api/gestion-notifications/', views.GestionNotificationsAPIView.as_view(), name='gestion-notifications'),
    path('api/marquer-notification-lue/<str:pk>/', views.GestionNotificationsAPIView.as_view(), name='marquer-notification-lue'),
    
    # Interface DRF
    path('api-auth/', include('rest_framework.urls')),
]