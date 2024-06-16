from flask import Flask, request, jsonify
from joblib import load
import streamlit as st
import requests
import json
import threading

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Fungsi untuk memuat model
def load_model():
    global DTReg
    DTReg = load('windprediction_DTReg.pkl')

# Muat model saat aplikasi dijalankan
load_model()

# Endpoint untuk memprediksi
@app.route('/predict', methods=['POST'])
def predict():
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
        return jsonify({'error': str(e)}), 500

# Fungsi untuk menjalankan Flask di thread terpisah
def run_flask():
    app.run(host="0.0.0.0", port=80, threaded=True)

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
    if response.status_code == 200:
        result = response.json()
        if 'ff_x' in result:
            st.success(f"Prediction: {result['ff_x']}")
        else:
            st.error('Error in prediction response')
    else:
        st.error('Error in prediction')
