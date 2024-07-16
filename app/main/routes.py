from flask import request, jsonify, Blueprint, current_app
from app.main import main
import os
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import uuid

model_path = os.path.join(os.path.dirname(__file__), '../model/model_race_gender_detect.h5')
model = load_model(model_path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def preprocess_image(image_path):
    img = load_img(image_path, target_size=(198, 198))
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

@main.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        img = preprocess_image(file_path)
        predictions = model.predict(img)
        
        race_pred = np.argmax(predictions[0], axis=1)[0]
        gender_pred = np.argmax(predictions[1], axis=1)[0]
        
        race_dict = {0: 'white', 1: 'black', 2: 'asian', 3: 'indian', 4: 'others'}
        gender_dict = {0: 'male', 1: 'female'}
        
        race = race_dict[race_pred]
        gender = gender_dict[gender_pred]
        
        return jsonify({
            "race": race,
            "gender": gender
        })
    
    return jsonify({"error": "Invalid file type"}), 400
