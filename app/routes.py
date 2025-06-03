from flask import Blueprint, request, jsonify, render_template
import requests
from .firebase_utils import upload_plate_data

bp = Blueprint('routes', __name__)

API_TOKEN = 'd81dc1b204aea00b9e846861cee62bb8dd2e2c0b'
@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['image']
        regions = ['sg', 'ph']

        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data={'regions': regions, 'mmc' : 'true'},
            files={'upload': file},
            headers={'Authorization': f'Token {API_TOKEN}'}
        )

        if response:
            result = response.json()

            if result['results']:
                top_result = result['results'][0]
                plate_number = top_result.get('plate')
                vehicle_type = top_result.get('vehicle', {}).get('type', 'Unknown')
                color_list = top_result.get('color', [])
                if color_list:
                  color = color_list[0].get('color', 'Unknown')
                else:
                   color = 'Unknown'

                timestamp = result.get('timestamp', 'N/A')

                data_result = {
                    "Plate Number": plate_number,
                    "Vehicle Type": vehicle_type,
                    "Timestamp": timestamp,
                    "Color": color
                }

                upload_plate_data(data_result)
                return jsonify(data_result), 200

       
            return jsonify({'error': 'No plate found in the image'}), 404

        return jsonify({'error': 'Failed to process image'}), 400
