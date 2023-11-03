import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('../Dataset/processed_data.csv') 
data = data.tail(60)
average_pm25 = data['PM 2.5'].mean()

if 0 <= average_pm25 <= 50:
    Ia = 100
    Ib = 50
    Xa = 55.4
    Xb = 15.5
    color = 'green'
    health_status = 'Baik'
elif 51 <= average_pm25 <= 100:
    Ia = 200
    Ib = 100
    Xa = 150.4
    Xb = 55.4
    color = 'blue'
    health_status = 'Sedang'
elif 101 <= average_pm25 <= 200:
    Ia = 300
    Ib = 200
    Xa = 250.4
    Xb = 150.4
    color = 'yellow'
    health_status = 'Tidak Sehat'
elif 201 <= average_pm25 <= 300:
    Ia = 400
    Ib = 300
    Xa = 500
    Xb = 250.4
    color = 'red'
    health_status = 'Sangat Tidak Sehat'
else:
    Ia = 500
    Ib = 500
    Xa = 500
    Xb = 500
    color = 'black'
    health_status = 'Berbahaya'


Xx = average_pm25
I = ((Ia - Ib) / (Xa - Xb)) * (Xx - Xb) + Ib


plt.plot(range(60), data['PM 2.5'], marker='o', color='blue')
plt.title('Grafik PM 2.5')
plt.xlabel('Data ke-')
plt.ylabel('PM 2.5')
plt.text(58, data['PM 2.5'].iloc[-1], health_status, color=color)
plt.xticks(range(60))
plt.grid()
plt.tight_layout()
plt.show()

print(f"Nilai rata-rata PM 2.5: {average_pm25}")
print(f"Ia: {Ia}, Ib: {Ib}, Xa: {Xa}, Xb: {Xb}")
print(f"Nilai I: {I}")
print(f"Status Kesehatan: {health_status}")
