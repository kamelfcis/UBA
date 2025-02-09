from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np

app = Flask(__name__)

# Load the trained model
model_path = 'Data/Mix/MLP.h5'
model = load_model(model_path)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    data = request.get_json(force=True)
    input_data = np.array(data['input']).reshape(1, -1)  # Reshape for a single prediction

    # Make prediction
    prediction = model.predict(input_data)
    predicted_class = np.argmax(prediction, axis=1)

    # Return the prediction as a JSON response
    return jsonify({'prediction': 'normal activity' if int(predicted_class[0]) == 1 else 'anomalous activity'})


if __name__ == '__main__':
    app.run(debug=True)
