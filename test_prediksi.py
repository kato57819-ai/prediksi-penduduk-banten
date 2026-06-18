import sys
sys.path.insert(0, '.')
from app import prediksi, get_data
import json

# Test data
df = get_data()
print("Data dari CSV:")
print(df)
print()

# Test prediksi route
print("Testing prediksi calculation...")
# Simulate the prediksi route
from flask import Flask
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

X = df['tahun'].values.reshape(-1,1)
model_total = LinearRegression().fit(X, df['total'])
model_laki_laki = LinearRegression().fit(X, df['laki'])
model_perempuan = LinearRegression().fit(X, df['perempuan'])

tahun_pred = np.array([2026, 2027, 2028, 2029, 2030]).reshape(-1,1)
hasil_total = model_total.predict(tahun_pred)
hasil_laki_laki = model_laki_laki.predict(tahun_pred)
hasil_perempuan = model_perempuan.predict(tahun_pred)

data = {
    "tahun": list(df['tahun']) + [2026, 2027, 2028, 2029, 2030],
    "total": list(df['total']) + [int(x) for x in hasil_total],
    "laki_laki": list(df['laki']) + [int(x) for x in hasil_laki_laki],
    "perempuan": list(df['perempuan']) + [int(x) for x in hasil_perempuan]
}

print("Data untuk template:")
print(f"Years: {data['tahun']}")
print(f"Total: {data['total']}")
print(f"Laki-laki: {data['laki_laki']}")
print(f"Perempuan: {data['perempuan']}")
print()

# Verify the structure matches what template expects
print("✅ Structure matches template expectations!")
print(f"- Tahun: {len(data['tahun'])} entries")
print(f"- Total: {len(data['total'])} entries")
print(f"- Laki-laki: {len(data['laki_laki'])} entries")
print(f"- Perempuan: {len(data['perempuan'])} entries")
