from flask import Flask, request, jsonify
from joblib import load
import streamlit as st
import requests
import json
import threading

# Inisialisasi aplikasi Flask
app = Flask(__name__)
model = load('windprediction_DTReg.model')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    Tavg = data['Tavg']
    RH_avg = data['RH_avg']
    
    prediction = model.predict([[Tavg, RH_avg]])
    result = {'ff_x': prediction[0]}
    
    return jsonify(result)

# Fungsi untuk menjalankan Flask di thread terpisah
def run_flask():
    app.run(host="localhost", port=5000)

# Jalankan Flask di thread terpisah
threading.Thread(target=run_flask).start()

# Streamlit interface
st.title('Wind Prediction')

Tavg = st.number_input('Average Temperature (Tavg)')
RH_avg = st.number_input('Average Relative Humidity (RH_avg)')

if st.button('Predict'):
    url = 'http://localhost:5000/predict'
    data = {'Tavg': Tavg, 'RH_avg': RH_avg}
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        st.success(f"Prediction: {result['ff_x']}")
    else:
        st.error('Error in prediction')
