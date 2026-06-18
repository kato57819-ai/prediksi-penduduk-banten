import os
import pandas as pd
import re

# Data ekstrak dari file BPS
data_yearly = []

# File-file yang ada
bps_files = [
    ('Jumlah Penduduk Menurut Kelompok Umur dan Jenis Kelamin di Provinsi Banten, 2020.csv', 2020),
    ('Jumlah Penduduk Menurut Kelompok Umur dan Jenis Kelamin di Provinsi Banten, 2023.csv', 2023),
    ('Jumlah Penduduk Menurut Kelompok Umur dan Jenis Kelamin (ribu jiwa) di Provinsi Banten, 2024.csv', 2024),
    ('Jumlah Penduduk Menurut Kelompok Umur dan Jenis Kelamin (ribu jiwa) di Provinsi Banten, 2025.csv', 2025),
]

def clean_number(num_str):
    """Convert Indonesian formatted number to integer"""
    if pd.isna(num_str):
        return None
    
    num_str = str(num_str).strip()
    
    # Remove spaces and replace European decimal separators
    # European format: 1.234.567,89 -> 1234567.89
    num_str = num_str.replace(' ', '')
    
    # If it has both . and ,
    if '.' in num_str and ',' in num_str:
        # Find last occurrence of both
        last_dot = num_str.rfind('.')
        last_comma = num_str.rfind(',')
        
        if last_comma > last_dot:
            # European format: 1.234.567,89
            num_str = num_str.replace('.', '').replace(',', '.')
        else:
            # English format: 1,234.56 (unlikely in BPS data)
            num_str = num_str.replace('.', '').replace(',', '')
    elif ',' in num_str:
        # Only comma - European decimal separator
        num_str = num_str.replace(',', '.')
    elif '.' in num_str:
        # Could be thousands separator only or decimal
        # Count dots - if more than 1, it's thousands separator
        dot_count = num_str.count('.')
        if dot_count > 1:
            num_str = num_str.replace('.', '')
    
    try:
        num_val = float(num_str)
        # If number is small (< 10000), assume it's in millions already displayed as decimal
        # Like 6.3209 means 6.3209 million
        if num_val < 10000:
            return int(num_val * 1000000)
        else:
            # If it's already large, it's in actual persons
            return int(num_val)
    except:
        return None

for filename, year in bps_files:
    filepath = os.path.join('', filename)
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
    
    try:
        df = pd.read_csv(filepath)
        
        # Ambil baris terakhir (Total/Jumlah)
        total_row = df.iloc[-1]
        
        # Extract values
        laki = clean_number(total_row.iloc[1])  # Column 1: Laki-laki
        perempuan = clean_number(total_row.iloc[2])  # Column 2: Perempuan
        total = laki + perempuan if laki and perempuan else None
        
        if total:
            data_yearly.append({
                'tahun': year,
                'total': total,
                'laki': laki,
                'perempuan': perempuan
            })
            print(f"{year}: {total:,} ({laki:,} L, {perempuan:,} P)")
    
    except Exception as e:
        print(f"Error processing {filename}: {e}")

# Sort by year
data_yearly.sort(key=lambda x: x['tahun'])

# Create DataFrame
df_result = pd.DataFrame(data_yearly)

# Interpolate missing years
all_years = pd.DataFrame({'tahun': range(2020, 2026)})
df_result = all_years.merge(df_result, on='tahun', how='left')
df_result = df_result.interpolate(method='linear', limit_direction='both')

# Round to integers
for col in ['total', 'laki', 'perempuan']:
    df_result[col] = df_result[col].round().astype(int)

# Save to CSV
df_result.to_csv('data_banten.csv', index=False)
print("\n✅ File data_banten.csv berhasil dibuat!")
print(df_result)
