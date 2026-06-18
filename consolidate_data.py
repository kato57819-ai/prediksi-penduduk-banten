"""
Script untuk mengkonsolidasi data penduduk dari tahun 2019-2025
ke dalam satu file CSV yang siap digunakan
"""

import pandas as pd
import glob
import re
from pathlib import Path

# List file yang akan diproses (dalam urutan tahun)
files_info = [
    ('Penduduk, Laju Pertumbuhan Penduduk, Distribusi Persentase Penduduk Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Kabupaten_Kota di Provinsi Banten, 2019.csv', 2019),
    ('Penduduk, Laju Pertumbuhan Penduduk, Distribusi Persentase Penduduk Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Kabupaten_Kota di Provinsi Banten, 2020.csv', 2020),
    ('Penduduk, Laju Pertumbuhan Penduduk, Distribusi Persentase Penduduk Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Kabupaten_Kota di Provinsi Banten, 2023.csv', 2023),
    ('Penduduk, Laju Pertumbuhan Penduduk, Distribusi Persentase Penduduk Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Kabupaten_Kota di Provinsi Banten, 2024.csv', 2024),
    ('Penduduk, Laju Pertumbuhan Penduduk, Distribusi Persentase Penduduk Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Kabupaten_Kota di Provinsi Banten, 2025.csv', 2025),
]

consolidated_data = []

for file_path, year in files_info:
    try:
        print(f"Membaca {file_path}...")
        df = pd.read_csv(file_path)
        
        # Hapus baris kosong dan baris "Catatan"
        df = df.dropna(subset=['Kabupaten/Kota'])
        df = df[~df['Kabupaten/Kota'].str.contains('Catatan|Hasil|hasil|<|>|Hasil', case=False, na=False, regex=True)]
        
        # Hapus baris total Banten jika ada (kita akan hitung ulang)
        df = df[df['Kabupaten/Kota'].str.strip() != 'Banten']
        
        # Filter hanya daerah utama (8-11 daerah Banten)
        valid_daerah = ['Pandeglang', 'Lebak', 'Tangerang', 'Serang', 
                        'Kota Tangerang', 'Kota Cilegon', 'Kota Serang', 
                        'Kota Tangerang Selatan', 'Kabupaten Tangerang', 'Kota Tangerang Selatan']
        
        # Filter df untuk hanya daerah yang valid
        df = df[df['Kabupaten/Kota'].isin(valid_daerah) | 
                df['Kabupaten/Kota'].str.contains('Pandeglang|Lebak|Tangerang|Serang|Cilegon', case=False, na=False)]
        
        # Tambah kolom tahun
        df['Tahun'] = year
        
        consolidated_data.append(df)
        print(f"✓ {file_path} berhasil dibaca ({len(df)} daerah)")
        
    except FileNotFoundError:
        print(f"✗ File tidak ditemukan: {file_path}")
    except Exception as e:
        print(f"✗ Error membaca {file_path}: {e}")

if consolidated_data:
    # Gabungkan semua data
    final_df = pd.concat(consolidated_data, ignore_index=True)
    
    # Rename kolom untuk lebih clean
    final_df = final_df.rename(columns={
        'Kabupaten/Kota': 'Kabupaten_Kota',
        'Jumlah Penduduk (Ribu)': 'Populasi_Ribu',
        'Laju Pertumbuhan Penduduk per Tahun': 'Laju_Pertumbuhan_Persen',
        'Persentase Penduduk': 'Persentase_Populasi',
        'Kepadatan Penduduk per km persegi (Km2)': 'Kepadatan_Per_Km2',
        'Rasio Jenis Kelamin Penduduk': 'Rasio_Jenis_Kelamin'
    })
    
    # Sort by tahun dan daerah
    final_df = final_df.sort_values(['Tahun', 'Kabupaten_Kota']).reset_index(drop=True)
    
    # Simpan ke CSV
    output_file = 'data_penduduk_konsolidasi_2019_2025.csv'
    final_df.to_csv(output_file, index=False)
    print(f"\n✓ Data berhasil dikonsolidasi ke: {output_file}")
    print(f"Total baris: {len(final_df)}")
    print(f"\nPreview data:")
    print(final_df.head(10))
    print(f"\n... (total {len(final_df)} baris)")
else:
    print("\n✗ Tidak ada data yang berhasil dibaca.")
