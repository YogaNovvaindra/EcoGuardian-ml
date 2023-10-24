import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Fungsi untuk membaca dataset
def read_dataset(file_path):
    data = pd.read_csv(file_path)
    return data

# Fungsi untuk melatih model
def train_model(X, y):
    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model

# Fungsi untuk membuat prediksi
def predict_next_data(model, new_data):
    prediksi = model.predict(new_data)
    return prediksi

if __name__ == "__main__":
    # Baca dataset awal
    data = read_dataset('smoke_detection_iot.csv')

    # Pisahkan fitur (features) dan target (target) dari dataset
    X = data[['UTC', 'Temperature[C]', 'Humidity[%]', 'TVOC[ppb]', 'eCO2[ppm]', 'Raw H2', 'Raw Ethanol', 'Pressure[hPa]', 'PM1.0', 'PM2.5', 'NC0.5', 'NC1.0', 'NC2.5', 'CNT']]
    y = data['Fire Alarm']

    # Ambil data dari baris 1 hingga 50 dari dataset sebagai data latihan
    data_latihan = X.iloc[1:51]
    target_latihan = y.iloc[1:51]

    # Latih model dengan data latihan
    trained_model = train_model(data_latihan, target_latihan)

    # Buat data input untuk prediksi secara otomatis
    data_input = X.iloc[51:52]  # Ambil baris ke-51 sebagai data input
    prediksi = predict_next_data(trained_model, data_input)

    # Cetak hasil prediksi
    print("Hasil Prediksi:", prediksi[0])

