from app import *
import json

# Test index
print('=== TEST INDEX ===')
df_latest = get_latest_year_data()
if df_latest is not None:
    print(f'✓ Data tahun {int(df_latest["Tahun"].iloc[0])} tersedia')
    print(f'✓ Jumlah daerah: {len(df_latest)}')
    print(f'✓ Total populasi: {int(df_latest["Populasi_Ribu"].sum() * 1000):,} jiwa')

# Test grafik
print()
print('=== TEST GRAFIK ===')
df = get_data()
latest_year = df['Tahun'].max()
df_latest_grafik = df[df['Tahun'] == latest_year].sort_values('Populasi_Ribu', ascending=False)
print(f'✓ Grafik tahun {int(latest_year)} siap')
print(f'✓ Top 3 daerah terbesar:')
for idx, (_, row) in enumerate(df_latest_grafik.head(3).iterrows(), 1):
    print(f'  {idx}. {row["Kabupaten_Kota"]}: {row["Populasi_Ribu"]:.1f} ribu jiwa')

# Test insight
print()
print('=== TEST INSIGHT ===')
first_year = df['Tahun'].min()
print(f'✓ Data historis: {int(first_year)}-{int(latest_year)} ({int(latest_year - first_year)} tahun)')
