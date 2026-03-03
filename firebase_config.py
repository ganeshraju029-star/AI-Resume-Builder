import os
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase with your service account
def initialize_firebase():
    try:
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            # Path to your service account key
            cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
            
            # Initialize Firebase Admin SDK
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'projectId': 'ai-resume-builder-b5dfc'
            })
        
        # Get Firestore database
        db = firestore.client()
        return db
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None

def get_firestore_db():
    """Get Firestore database instance"""
    try:
        return firestore.client()
    except Exception as e:
        print(f"Error getting Firestore client: {e}")
        return None

# Initialize database
db = initialize_firebase()
