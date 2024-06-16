from flask import Flask, request, jsonify
from joblib import load
import streamlit as st
import requests
import json
import threading
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
        logging.error("Model not loaded")
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        # Ambil data dari request POST
        data = request.get_json()
        Tavg = data['Tavg']
        RH_avg = data['RH_avg']
        
        # Lakukan prediksi dengan model
        prediction = DTReg.predict([[Tavg, RH_avg]])
        result = {'ff_x': prediction[0]}
        
        return jsonify(result)
    except Exception as e:
        logging.error("Prediction error: %s", e)
        return jsonify({'error': str(e)}), 500

# Fungsi untuk menjalankan Flask di thread terpisah
def run_flask():
    app.run(host="0.0.0.0", port=5000, threaded=True)

# Jalankan Flask di thread terpisah
threading.Thread(target=run_flask).start()

# Streamlit interface
st.title('Wind Prediction')

# Input dari pengguna untuk temperatur dan kelembaban relatif rata-rata
Tavg = st.number_input('Average Temperature (Tavg)')
RH_avg = st.number_input('Average Relative Humidity (RH_avg)')

# Tombol untuk melakukan prediksi
if st.button('Predict'):
    # Buat data untuk dikirim ke server Flask
    data = {'Tavg': Tavg, 'RH_avg': RH_avg}
    
    # URL endpoint prediksi (sesuaikan URL jika dideploy)
    url = 'https://wind-prediction-anemoi.streamlit.app/'
    
    # Headers untuk request POST
    headers = {'Content-Type': 'application/json'}
    
    # Kirim request POST ke server Flask
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Handle respons dari server Flask
    try:
        response.raise_for_status()  # Akan memunculkan error jika status code tidak 200
        result = response.json()  # Mencoba decode respons JSON
        if 'ff_x' in result:
            st.success(f"Prediction: {result['ff_x']}")
        else:
            st.error('Unexpected response structure')
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Request error occurred: {req_err}")
    except json.decoder.JSONDecodeError as json_err:
        st.error(f"JSON decode error occurred: {json_err}")
        st.error(f"Response content: {response.content.decode('utf-8')}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
