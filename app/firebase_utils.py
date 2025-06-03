import firebase_admin
from firebase_admin import credentials, db
import os
import json
from datetime import datetime


firebase_key_json = os.environ.get('FIREBASE_KEY')


firebase_key = json.loads(firebase_key_json)

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://plate-number-detection-a7574-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

def upload_plate_data(data):
    try:
        latest_id = db.reference('latest_id').get()
        if latest_id is None:
            latest_id = 1
        else:
            latest_id += 1

        db.reference('latest_id').set(latest_id)

        ref = db.reference(f'detected_plates/{latest_id}')
        ref.set({
            'plate_number': data.get('Plate Number', 'Not detected'),
            'vehicle_type': data.get('Vehicle Type', 'Unknown'),
            'timestamp': data.get('Timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        })
        return True
    except Exception as e:
        print(f"Error uploading to Firebase: {str(e)}")
        return False
