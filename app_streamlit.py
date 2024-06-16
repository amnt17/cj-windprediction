import streamlit as st
import requests
import json

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
    url = 'https://wind-prediction-anemoi.streamlit.app/'  # Ganti dengan URL Streamlit Sharing
    
    # Headers untuk request POST
    headers = {'Content-Type': 'application/json'}
    
    try:
        # Kirim request POST ke server Flask
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        
        # Handle respons dari server Flask
        result = response.json()
        if 'ff_x' in result:
            st.success(f"Prediction: {result['ff_x']}")
        else:
            st.error('Error in prediction response')
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error during request to Flask server: {e}")
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON response from Flask server: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
