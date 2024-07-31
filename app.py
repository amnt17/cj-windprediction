import pickle

# Gantilah 'path/to/your/file.pkl' dengan path ke file .pkl Anda
file_path = 'windprediction_DTReg.pkl'

with open(file_path, 'rb') as file:
    data = pickle.load(file)

# Tampilkan atau gunakan data yang telah di-load
print(data)
