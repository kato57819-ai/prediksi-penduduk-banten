from app import get_data
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error

df = get_data()
daerah_test = 'Tangerang'
df_test = df[df['Kabupaten_Kota'] == daerah_test].sort_values('Tahun')

X = df_test['Tahun'].values.reshape(-1, 1)
y = df_test['Populasi_Ribu'].values

# Multiple Linear Regression dengan Polynomial degree 2
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)

y_pred = model.predict(X_poly)
r2 = r2_score(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))

# Prediksi tahun depan
tahun_future = np.array([2026, 2027, 2028, 2029, 2030]).reshape(-1, 1)
X_future_poly = poly.transform(tahun_future)
y_future = model.predict(X_future_poly)

print(f"Daerah: {daerah_test}")
print(f"R² Score: {r2:.4f} (model accuracy)")
print(f"RMSE: {rmse:.2f} ribu jiwa")
print()
print("Prediksi Tahun Depan:")
for tahun, populasi in zip([2026, 2027, 2028, 2029, 2030], y_future):
    print(f"  {tahun}: {populasi:.1f} ribu jiwa")
