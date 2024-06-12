from flask import Flask, request, jsonify
from joblib import load
import streamlit as st
import requests 
import json
import threading

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Fungsi untuk memuat model saat aplikasi Flask dijalankan
def load_model():
    global model
    model = load('windprediction_DTReg.pkl')

# Endpoint untuk memprediksi
@app.route('/predict', methods=['POST'])
def predict():
    # Ambil data dari request POST
    data = request.get_json()
    Tavg = data['Tavg']
    RH_avg = data['RH_avg']
    
    # Lakukan prediksi dengan model
    prediction = model.predict([[Tavg, RH_avg]])
    result = {'ff_x': prediction[0]}
    
    return jsonify(result)

# Fungsi untuk menjalankan Flask di thread terpisah
def run_flask():
    app.run(host="localhost", port=5000)

# Jalankan fungsi load_model di thread terpisah
threading.Thread(target=load_model).start()

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
    
    # URL endpoint prediksi
    url = 'http://localhost:5000/predict'
    
    # Headers untuk request POST
    headers = {'Content-Type': 'application/json'}
    
    # Kirim request POST ke server Flask
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Handle respons dari server Flask
    if response.status_code == 200:
        result = response.json()
        st.success(f"Prediction: {result['ff_x']}")
    else:
        st.error('Error in prediction')
