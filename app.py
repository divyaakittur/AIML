import base64
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin # Import flask_cors
from predictt import predict_img
import json

import numpy as np
from PIL import Image
import tensorflow as tf

# Initialize Flask app

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Load your machine learning model
# model = tf.keras.models.load_model('path_to_your_model')

# Define a function to process the image and make predictions


# Define the API endpoint for image processing
@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    # try:
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    image.save("input.png")
    predict_img("input.png")
    with open("output.jpeg",'rb') as f:
        img=base64.b64encode(f.read()).decode("utf-8")
    #     img_array = process_image(image)
    #
    #     # Make predictions using the loaded model
    #     predictions = model.predict(img_array)
    #     # Assuming a classification model, you can get the predicted class label
    #     predicted_class = np.argmax(predictions)
    #
    #     return jsonify({'predicted_class': int(predicted_class)})
    return json.dumps({'img': img})
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
