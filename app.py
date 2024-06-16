from flask import Flask, request, jsonify
from joblib import load
import logging

# Inisialisasi logging
logging.basicConfig(level=logging.DEBUG)

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Fungsi untuk memuat model
def load_model():
    global DTReg
    try:
        DTReg = load('windprediction_DTReg.pkl')
        logging.info("Model loaded successfully.")
    except Exception as e:
        logging.error("Error loading model: %s", e)
        DTReg = None

# Muat model saat aplikasi dijalankan
load_model()

# Endpoint untuk memprediksi
@app.route('/predict', methods=['POST'])
def predict():
    if DTReg is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        # Ambil data dari request POST
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        Tavg = data['Tavg']
        RH_avg = data['RH_avg']
        
        # Lakukan prediksi dengan model
        prediction = DTReg.predict([[Tavg, RH_avg]])
        result = {'ff_x': prediction[0]}
        
        logging.debug(f"Sending result: {result}")
        return jsonify(result)
    except Exception as e:
        logging.error("Prediction error: %s", e)
        return jsonify({'error': str(e)}), 500

# Menjalankan Flask di thread terpisah
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, threaded=True)
