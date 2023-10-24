import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Step 1: Data Preparation
data = pd.read_csv("smoke_detection_iot.csv")
new_data = pd.read_csv("new_data.csv")
data = pd.concat([data, new_data], ignore_index=True)

features = data.drop(columns=["UTC", "Humidity[%]"])
target = data["Humidity[%]"]

# Step 2: Data Splitting
random_state = 42
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=random_state)

# Step 3: Data Preprocessing
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 4: Membuat dan Melatih Model Deep Learning dengan Regresi yang Lebih Mendalam
model_deep = keras.Sequential([
    keras.layers.Input(shape=(X_train_scaled.shape[1],)),
    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dense(256, activation='relu'), 
    keras.layers.Dense(128, activation='relu'),  
    keras.layers.Dense(64, activation='relu'),  
    keras.layers.Dense(32, activation='relu'),  
    keras.layers.Dense(128, activation='relu'),  
    keras.layers.Dense(1, activation='linear')  
])

# Sekarang, Anda dapat melanjutkan dengan sisa kode Anda

model_deep.add(keras.layers.Dropout(0.1))  # Regularisasi dropout

model_deep.compile(loss='mse', optimizer='adam', loss_weights=[1.0, 0.00001])  # Regularisasi L2

early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

model_deep.fit(X_train_scaled, y_train, validation_data=(X_test_scaled, y_test), epochs=100, batch_size=32, callbacks=[early_stopping])

# Step 5: Evaluasi Model Deep Learning dengan Regresi yang Lebih Mendalam
y_pred_deep = model_deep.predict(X_test_scaled)

mae_deep = mean_absolute_error(y_test, y_pred_deep)
mse_deep = mean_squared_error(y_test, y_pred_deep)
r2_deep = r2_score(y_test, y_pred_deep)

print("Evaluasi Model Deep Learning (Regresi yang Lebih Mendalam):")
print(f"Mean Absolute Error: {mae_deep}")
print(f"Mean Squared Error: {mse_deep}")
print(f"R-squared: {r2_deep}")

# Step 6: Prediksi Kelembapan Tanah dengan Model Deep Learning (Regresi yang Lebih Mendalam)
data_prediksi = data.iloc[0]  
data_prediksi = data_prediksi.drop(["UTC", "Humidity[%]"]) 
data_prediksi = scaler.transform(data_prediksi.values.reshape(1, -1))  

predicted_humidity_deep = model_deep.predict(data_prediksi)
print(f"Prediksi Kelembapan Tanah (Deep Learning - Regresi yang Lebih Mendalam): {predicted_humidity_deep[0][0]}")
