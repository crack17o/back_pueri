"""
Script d'initialisation des données de test pour le système de gestion scolaire
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_scolaire.settings')
django.setup()

from core.models import *
from core.services import AuthTokenService

def create_sample_data():
    """Crée des données d'exemple pour tester le système"""
    
    print("🚀 Initialisation des données de test...")
    
    # 1. Créer des utilisateurs
    print("👥 Création des utilisateurs...")
    
    # Développeur
    dev_user = User(
        nom="Dupont",
        prenom="Jean",
        email="dev@school.com",
        motDePasse="dev123",
        role="developpeur",
        telephone="0123456789"
    )
    dev_user.save()
    
    # Administrateur
    admin_user = User(
        nom="Martin",
        prenom="Sophie",
        email="admin@school.com",
        motDePasse="admin123",
        role="admin",
        telephone="0123456790"
    )
    admin_user.save()
    
    # Professeurs
    professeurs = []
    prof_data = [
        ("Durand", "Pierre", "prof.math@school.com", "prof123"),
        ("Moreau", "Marie", "prof.francais@school.com", "prof123"),
        ("Petit", "Paul", "prof.anglais@school.com", "prof123"),
        ("Bernard", "Anne", "prof.sciences@school.com", "prof123"),
    ]
    
    for nom, prenom, email, pwd in prof_data:
        prof = User(
            nom=nom,
            prenom=prenom,
            email=email,
            motDePasse=pwd,
            role="professeur",
            telephone=f"012345{len(professeurs)+1:04d}"
        )
        prof.save()
        professeurs.append(prof)
    
    # Parents
    parents = []
    parent_data = [
        ("Leblanc", "Michel", "parent1@school.com"),
        ("Roux", "Catherine", "parent2@school.com"),
        ("Garnier", "Philippe", "parent3@school.com"),
        ("Faure", "Isabelle", "parent4@school.com"),
    ]
    
    for nom, prenom, email in parent_data:
        parent = User(
            nom=nom,
            prenom=prenom,
            email=email,
            motDePasse="parent123",
            role="parent",
            telephone=f"012345{len(parents)+2000:04d}"
        )
        parent.save()
        parents.append(parent)
    
    print(f"✅ {len(professeurs)} professeurs et {len(parents)} parents créés")
    
    # 2. Créer des classes
    print("🏫 Création des classes...")
    
    classes_data = [
        ("CP", 1, "primaire", 10, [("A", professeurs[0]), ("B", professeurs[1])]),
        ("CE1", 2, "primaire", 10, [("A", professeurs[0]), ("B", professeurs[1])]),
        ("6ème", 7, "secondaire", 12, [("A", None), ("B", None)]),
        ("5ème", 8, "secondaire", 12, [("A", None), ("B", None)]),
    ]
    
    classes = []
    for nom, niveau, type_classe, seuil, subdivisions_info in classes_data:
        subdivisions = []
        for sub_nom, prof in subdivisions_info:
            subdivision = Subdivision(nom=sub_nom, profPrincipal=prof)
            subdivisions.append(subdivision)
        
        classe = Classe(
            nom=nom,
            niveau=niveau,
            typeClasse=type_classe,
            seuilPromotion=seuil,
            subdivisions=subdivisions
        )
        classe.save()
        classes.append(classe)
    
    print(f"✅ {len(classes)} classes créées")
    
    # 3. Créer des matières
    print("📚 Création des matières...")
    
    matieres_data = [
        ("Mathématiques", 4, professeurs[0]),
        ("Français", 4, professeurs[1]),
        ("Anglais", 2, professeurs[2]),
        ("Sciences", 3, professeurs[3]),
    ]
    
    matieres = []
    for nom, coeff, prof in matieres_data:
        # Créer la matière pour chaque classe secondaire
        for classe in classes:
            if classe.typeClasse == "secondaire":
                matiere = Matiere(
                    nom=nom,
                    coefficient=coeff,
                    professeur=prof,
                    classe=classe
                )
                matiere.save()
                matieres.append(matiere)
    
    print(f"✅ {len(matieres)} matières créées")
    
    # 4. Créer des élèves
    print("🎓 Création des élèves...")
    
    eleves_data = [
        ("Élève1", "Prénom1", "E001", parents[0:2]),
        ("Élève2", "Prénom2", "E002", parents[1:3]),
        ("Élève3", "Prénom3", "E003", parents[2:4]),
        ("Élève4", "Prénom4", "E004", parents[0:1]),
        ("Élève5", "Prénom5", "E005", parents[1:2]),
        ("Élève6", "Prénom6", "E006", parents[2:3]),
    ]
    
    eleves = []
    for nom, prenom, matricule, eleve_parents in eleves_data:
        classe_choisie = random.choice(classes)
        subdivision_choisie = random.choice([sub.nom for sub in classe_choisie.subdivisions])
        
        eleve = Eleve(
            nom=nom,
            prenom=prenom,
            matricule=matricule,
            dateNaissance=datetime.now() - timedelta(days=random.randint(3650, 5475)),  # 10-15 ans
            classe=classe_choisie,
            subdivision=subdivision_choisie,
            parents=eleve_parents,
            methodeSubdivision="auto"
        )
        eleve.save()
        eleves.append(eleve)
        
        # Mettre à jour les références des parents
        for parent in eleve_parents:
            parent.enfants.append(eleve)
            parent.save()
    
    print(f"✅ {len(eleves)} élèves créés")
    
    # 5. Créer une année scolaire avec trimestres et périodes
    print("📅 Création de l'année scolaire...")
    
    annee = AnneeScolaire(
        nom="2024-2025",
        dateDebut=datetime(2024, 9, 1),
        dateFin=datetime(2025, 6, 30)
    )
    annee.save()
    
    # Trimestres
    trimestres = []
    trimestre_data = [
        ("Trimestre 1", datetime(2024, 9, 1), datetime(2024, 12, 20)),
        ("Trimestre 2", datetime(2025, 1, 7), datetime(2025, 4, 4)),
        ("Trimestre 3", datetime(2025, 4, 21), datetime(2025, 6, 30)),
    ]
    
    for nom, debut, fin in trimestre_data:
        trimestre = Trimestre(
            nom=nom,
            dateDebut=debut,
            dateFin=fin,
            anneeScolaire=annee
        )
        trimestre.save()
        trimestres.append(trimestre)
        
        # Périodes pour chaque trimestre
        periode1 = Periode(
            nom=f"Période 1 - {nom}",
            dateDebut=debut,
            dateFin=debut + timedelta(days=45),
            trimestre=trimestre
        )
        periode1.save()
        
        periode2 = Periode(
            nom=f"Période 2 - {nom}",
            dateDebut=debut + timedelta(days=46),
            dateFin=fin,
            trimestre=trimestre
        )
        periode2.save()
        
        trimestre.periodes = [periode1, periode2]
        trimestre.save()
    
    annee.trimestres = trimestres
    annee.save()
    
    print(f"✅ Année scolaire avec {len(trimestres)} trimestres créée")
    
    # 6. Créer quelques devoirs
    print("📝 Création des devoirs...")
    
    devoirs_data = [
        ("Devoir de Mathématiques", "Exercices sur les fractions", professeurs[0]),
        ("Rédaction en Français", "Écrire une histoire courte", professeurs[1]),
        ("Test d'Anglais", "Vocabulaire et grammaire", professeurs[2]),
    ]
    
    devoirs = []
    for titre, description, prof in devoirs_data:
        classe_choisie = random.choice(classes)
        subdivision_choisie = random.choice([sub.nom for sub in classe_choisie.subdivisions])
        
        devoir = Devoir(
            titre=titre,
            description=description,
            dateLimite=datetime.now() + timedelta(days=7),
            classe=classe_choisie,
            subdivision=subdivision_choisie,
            matiere=random.choice(matieres) if matieres else None,
            professeur=prof
        )
        devoir.save()
        devoirs.append(devoir)
    
    print(f"✅ {len(devoirs)} devoirs créés")
    
    print("🎉 Initialisation terminée avec succès!")
    print("✅ Données d'exemple créées avec succès !")
    
    # Créer des tokens pour tous les utilisateurs de test
    print("🔐 Génération des tokens...")
    tokens_crees = 0
    for user in User.objects.all():
        token = AuthTokenService.create_token(user)
        tokens_crees += 1
        print(f"   Token pour {user.email}: {token.key}")
    
    print(f"✅ {tokens_crees} tokens créés")
    
    print("🎉 Initialisation terminée avec succès!")
    print(f"""
📊 Récapitulatif des données créées :
   • {User.objects.count()} utilisateurs
   • {Classe.objects.count()} classes
   • {Matiere.objects.count()} matières
   • {Eleve.objects.count()} élèves
   • {AnneeScolaire.objects.count()} année scolaire
   • {Trimestre.objects.count()} trimestres
   • {Periode.objects.count()} périodes
   • {Devoir.objects.count()} devoirs

🔑 Comptes de test :
   • Développeur : dev@school.com / dev123
   • Administrateur : admin@school.com / admin123
   • Professeur : prof.math@school.com / prof123
   • Parent : parent1@school.com / parent123

💡 Utilisez ces comptes pour tester l'API !
📡 Base URL : http://localhost:8000/api/
🔐 Auth URL : http://localhost:8000/api/auth/
""")

if __name__ == "__main__":
    try:
        create_sample_data()
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        import traceback
        traceback.print_exc()
