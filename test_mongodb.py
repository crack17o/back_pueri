import os
import django
import pymongo

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_scolaire.settings')
django.setup()

def test_mongo_connection():
    try:
        # Test direct avec pymongo
        client = pymongo.MongoClient(
            "mongodb+srv://jelly:bJByktwM0hRaT0xU@cluster0.94mrjki.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        
        # Tester la connexion
        db = client.gestion_scolaire_db
        collections = db.list_collection_names()
        print(f"✅ Connexion MongoDB réussie! Collections: {collections}")
        
        # Tester avec mongoengine
        from core.models import User
        count = User.objects.count()
        print(f"✅ MongoEngine fonctionne! Utilisateurs: {count}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_mongo_connection()