import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_scolaire.settings')
django.setup()

from datetime import datetime
from core.models import *

def init_database():
    print("🚀 Initialisation des données de test...")
    
    # 1. Créer des utilisateurs
    admin_user = User(
        nom="Admin",
        prenom="System",
        email="admin@ecole.com",
        motDePasse="admin123",
        role="admin",
        telephone="+1234567890"
    )
    admin_user.save()
    
    prof_user = User(
        nom="Professeur",
        prenom="Math",
        email="prof@ecole.com", 
        motDePasse="prof123",
        role="professeur",
        telephone="+1234567891"
    )
    prof_user.save()
    
    parent_user = User(
        nom="Parent",
        prenom="Eleve",
        email="parent@ecole.com",
        motDePasse="parent123", 
        role="parent",
        telephone="+1234567892"
    )
    parent_user.save()
    
    # 2. Créer une année scolaire
    annee_scolaire = AnneeScolaire(
        nom="2024-2025",
        dateDebut=datetime(2024, 9, 1),
        dateFin=datetime(2025, 7, 31)
    )
    annee_scolaire.save()
    
    # 3. Créer des classes
    classe_cp = Classe(
        nom="CP1",
        niveau=1,
        typeClasse="primaire",
        seuilPromotion=50
    )
    classe_cp.save()
    
    classe_ce1 = Classe(
        nom="CE1", 
        niveau=2,
        typeClasse="primaire",
        seuilPromotion=50
    )
    classe_ce1.save()
    
    # 4. Créer des élèves
    eleve1 = Eleve(
        nom="Dupont",
        prenom="Marie",
        matricule="ELEVE001",
        dateNaissance=datetime(2018, 5, 15),
        classe=classe_cp,
        parents=[parent_user]
    )
    eleve1.save()
    
    eleve2 = Eleve(
        nom="Martin", 
        prenom="Pierre",
        matricule="ELEVE002",
        dateNaissance=datetime(2018, 3, 20),
        classe=classe_cp,
        parents=[parent_user]
    )
    eleve2.save()
    
    # 5. Créer des matières
    maths = Matiere(
        nom="Mathématiques",
        coefficient=4,
        professeur=prof_user,
        classe=classe_cp
    )
    maths.save()
    
    francais = Matiere(
        nom="Français",
        coefficient=4, 
        professeur=prof_user,
        classe=classe_cp
    )
    francais.save()
    
    print("✅ Données initialisées avec succès!")
    print(f"👥 {User.objects.count()} utilisateurs créés")
    print(f"🎓 {Eleve.objects.count()} élèves créés") 
    print(f"📚 {Classe.objects.count()} classes créées")
    print(f"📖 {Matiere.objects.count()} matières créées")

if __name__ == "__main__":
    init_database()