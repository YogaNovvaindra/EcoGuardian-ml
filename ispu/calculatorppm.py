def konversi_ppm_ke_ug_m3(ppm, berat_molekul, volume_molar, pangkat=1000):
    return ((ppm * berat_molekul) / volume_molar) * pangkat

# Nilai dari contoh perhitungan
ppm_CO = 1.52
berat_molekul_CO = 28.01  # Berat molekul CO dalam g/mol
volume_molar_CO = 24.5  # Volume molar CO dalam L/mol

# Melakukan perhitungan konversi
konsentrasi_ug_m3_CO = konversi_ppm_ke_ug_m3(ppm_CO, berat_molekul_CO, volume_molar_CO)

# Menampilkan hasil
print(f"Konsentrasi CO: {konsentrasi_ug_m3_CO:.2f} µg/m³")
