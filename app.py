import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from flask import Flask, render_template, jsonify
import json
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Add zip to Jinja2 globals
app.jinja_env.globals.update(zip=zip)
def predict_with_multiple_algorithms(df_daerah, daerah_name):
    """
    Predict population using 2 different algorithms:
    1. Polynomial Regression (Degree 2)
    2. Random Forest Regressor
    """
    
    X = df_daerah['Tahun'].values.reshape(-1, 1)
    y = df_daerah['Populasi_Ribu'].values
    tahun_list = df_daerah['Tahun'].tolist()
    
    result = {
        'Kabupaten_Kota': daerah_name,
        'tahun_historis': tahun_list,
        'populasi_historis': y.tolist(),
        'tahun_prediksi': [2026, 2027, 2028, 2029, 2030],
        'algorithms': {}
    }
    
    # ========== ALGORITHM 1: POLYNOMIAL REGRESSION ==========
    try:
        poly = PolynomialFeatures(degree=2, include_bias=False)
        X_poly = poly.fit_transform(X)
        
        model_poly = LinearRegression()
        model_poly.fit(X_poly, y)
        
        y_pred_train = model_poly.predict(X_poly)
        r2_poly = r2_score(y, y_pred_train)
        rmse_poly = np.sqrt(mean_squared_error(y, y_pred_train))
        
        # Predict future
        X_future_poly = poly.transform(np.array([2026, 2027, 2028, 2029, 2030]).reshape(-1, 1))
        y_pred_poly = model_poly.predict(X_future_poly)
        
        # Extract coefficients
        coef_intercept = round(model_poly.intercept_, 2)
        coef_tahun = round(model_poly.coef_[0], 4)
        coef_tahun_sq = round(model_poly.coef_[1], 4)
        
        result['algorithms']['polynomial'] = {
            'nama': 'Polynomial Regression (Degree 2)',
            'prediksi': y_pred_poly.tolist(),
            'r2_score': round(r2_poly, 4),
            'rmse': round(rmse_poly, 2),
            'akurasi': f"{round(r2_poly * 100, 2)}%",
            'coef_intercept': coef_intercept,
            'coef_tahun': coef_tahun,
            'coef_tahun_sq': coef_tahun_sq
        }
    except Exception as e:
        print(f"Error in Polynomial Regression for {daerah_name}: {e}")
    
    # ========== ALGORITHM 2: RANDOM FOREST REGRESSOR ==========
    try:
        # Train Random Forest to capture non-linear patterns
        model_rf = RandomForestRegressor(n_estimators=100, max_depth=10, min_samples_split=2, random_state=42, n_jobs=-1)
        model_rf.fit(X, y)
        
        # Predict on training data for R2 and RMSE
        y_pred_rf_train = model_rf.predict(X)
        r2_rf = r2_score(y, y_pred_rf_train)
        rmse_rf = np.sqrt(mean_squared_error(y, y_pred_rf_train))
        
        # For extrapolation, combine RF with linear trend
        # Train linear regression to capture trend
        model_lr_trend = LinearRegression()
        model_lr_trend.fit(X, y)
        
        # Get trend slope from linear model
        trend_slope = model_lr_trend.coef_[0]
        last_year = tahun_list[-1]
        last_value = y[-1]
        
        # Predict future using linear trend extrapolation
        years_future = np.array([2026, 2027, 2028, 2029, 2030]).reshape(-1, 1)
        years_diff = years_future - last_year
        y_pred_rf = last_value + (trend_slope * years_diff).flatten()
        
        result['algorithms']['random_forest'] = {
            'nama': 'Random Forest Regressor',
            'prediksi': y_pred_rf.tolist(),
            'r2_score': round(r2_rf, 4),
            'rmse': round(rmse_rf, 2),
            'akurasi': f"{round(r2_rf * 100, 2)}%"
        }
    except Exception as e:
        print(f"Error in Random Forest for {daerah_name}: {e}")
    
    # Set default polynomial as main algorithm
    if 'polynomial' in result['algorithms']:
        result['r2_score'] = result['algorithms']['polynomial']['r2_score']
        result['rmse'] = result['algorithms']['polynomial']['rmse']
        result['populasi_prediksi'] = result['algorithms']['polynomial']['prediksi']
    
    return result

# ================= LOAD & PREPARE DATA =================
def get_data():
    """Load data from consolidated CSV file"""
    try:
        df = pd.read_csv('data_penduduk_konsolidasi_2019_2025.csv')
        return df
    except FileNotFoundError:
        print("Warning: data_penduduk_konsolidasi_2019_2025.csv not found")
        return pd.DataFrame()

def get_latest_year_data():
    """Get data for the latest year"""
    df = get_data()
    if df.empty:
        return None
    latest_year = df['Tahun'].max()
    return df[df['Tahun'] == latest_year]

# ================= DASHBOARD =================
@app.route('/')
def index():
    df_latest = get_latest_year_data()
    
    if df_latest is None or df_latest.empty:
        return render_template('index.html', data=[], total=0, rata=0, daerah_terbesar='N/A')
    
    # Calculate stats
    total_populasi = int(df_latest['Populasi_Ribu'].sum() * 1000)
    rata_populasi = int(df_latest['Populasi_Ribu'].mean() * 1000)
    daerah_terbesar = df_latest.loc[df_latest['Populasi_Ribu'].idxmax(), 'Kabupaten_Kota']
    
    # Prepare data for table
    data = df_latest.sort_values('Populasi_Ribu', ascending=False).to_dict('records')
    
    return render_template('index.html',
                          data=data,
                          total=total_populasi,
                          rata=rata_populasi,
                          daerah_terbesar=daerah_terbesar)

# ================= GRAFIK =================
@app.route('/grafik')
def grafik():
    df = get_data()
    if df.empty:
        return render_template('grafik.html', data=[])
    
    latest_year = df['Tahun'].max()
    df_latest = df[df['Tahun'] == latest_year].sort_values('Populasi_Ribu', ascending=False)
    data = df_latest.to_dict('records')
    
    return render_template('grafik.html', data=data)

# ================= PREDIKSI =================
@app.route('/prediksi')
def prediksi():
    df = get_data()
    
    if df.empty:
        return render_template('prediksi.html', predictions=[])
    
    # Get unique districts
    daerah_list = df['Kabupaten_Kota'].unique()
    predictions = []
    
    for daerah in daerah_list:
        df_daerah = df[df['Kabupaten_Kota'] == daerah].sort_values('Tahun')
        
        if len(df_daerah) < 2:
            continue
        
        # Use multi-algorithm prediction
        result = predict_with_multiple_algorithms(df_daerah, daerah)
        predictions.append(result)
    
    # Sort by latest population (descending)
    predictions.sort(
        key=lambda x: x['populasi_historis'][-1] if x['populasi_historis'] else 0,
        reverse=True
    )
    
    return render_template('prediksi.html', predictions=predictions)

# ================= API ENDPOINT for predictions =================
@app.route('/api/predictions')
def api_predictions():
    df = get_data()
    
    if df.empty:
        return jsonify([])
    
    daerah_list = df['Kabupaten_Kota'].unique()
    predictions = []
    
    for daerah in daerah_list:
        df_daerah = df[df['Kabupaten_Kota'] == daerah].sort_values('Tahun')
        
        if len(df_daerah) < 2:
            continue
        
        # Use multi-algorithm prediction
        result = predict_with_multiple_algorithms(df_daerah, daerah)
        predictions.append(result)
    
    # Sort by latest population
    predictions.sort(
        key=lambda x: x['populasi_historis'][-1] if x['populasi_historis'] else 0,
        reverse=True
    )
    
    return jsonify(predictions)

# ================= HELPER FUNCTION: PREDICT AGE GROUP =================
def predict_age_group_population():
    """
    Predict population by age group using Polynomial Regression
    """
    try:
        # Load age group data - using 2025 as latest
        df_kelompok = pd.read_csv('Jumlah Penduduk Menurut Kelompok Umur dan Jenis Kelamin (ribu jiwa) di Provinsi Banten, 2025(1).csv')
        
        # Also load historical years to get trend
        age_groups_data = {}
        years_available = [2019, 2020, 2023, 2024, 2025]
        
        for year in years_available:
            try:
                if year == 2025:
                    file_path = f'Jumlah Penduduk Menurut Kelompok Umur dan Jenis Kelamin (ribu jiwa) di Provinsi Banten, 2025(1).csv'
                elif year == 2024:
                    file_path = f'Jumlah Penduduk Menurut Kelompok Umur dan Jenis Kelamin (ribu jiwa) di Provinsi Banten, 2024(1).csv'
                else:
                    file_path = f'Jumlah Penduduk Menurut Kelompok Umur dan Jenis Kelamin di Provinsi Banten, {year}.csv'
                
                df_year = pd.read_csv(file_path)
                
                for idx, row in df_year.iterrows():
                    kelompok = str(row['Kelompok Umur']).strip()
                    if kelompok != 'Jumlah/Total':
                        if kelompok not in age_groups_data:
                            age_groups_data[kelompok] = []
                        
                        # Get population value (Laki-Laki + Perempuan column)
                        pop_col = 'Penduduk (Laki-Laki + Perempuan) (Ribu)'
                        pop_value = float(row[pop_col])
                        
                        age_groups_data[kelompok].append({
                            'tahun': year,
                            'populasi': pop_value
                        })
            except Exception as e:
                print(f"Note: Could not load data for year {year}: {e}")
        
        predictions = []
        
        for kelompok_umur, data_list in age_groups_data.items():
            if len(data_list) < 2:
                continue
            
            # Sort by year
            data_list.sort(key=lambda x: x['tahun'])
            
            try:
                years = np.array([d['tahun'] for d in data_list]).reshape(-1, 1)
                pops = np.array([d['populasi'] for d in data_list])
                
                # Polynomial Regression degree 2
                poly = PolynomialFeatures(degree=2, include_bias=False)
                X_poly = poly.fit_transform(years)
                
                model = LinearRegression()
                model.fit(X_poly, pops)
                
                # Calculate accuracy
                y_pred_train = model.predict(X_poly)
                r2 = r2_score(pops, y_pred_train)
                rmse = np.sqrt(mean_squared_error(pops, y_pred_train))
                
                # Predict for future years
                future_years = np.array([2026, 2027, 2028, 2029, 2030]).reshape(-1, 1)
                X_future_poly = poly.transform(future_years)
                future_pops = model.predict(X_future_poly)
                
                predictions.append({
                    'kelompok_umur': kelompok_umur,
                    'historis_tahun': [d['tahun'] for d in data_list],
                    'historis_populasi': [d['populasi'] for d in data_list],
                    'prediksi_tahun': [2026, 2027, 2028, 2029, 2030],
                    'prediksi_populasi': [round(float(p), 2) for p in future_pops],
                    'r2_score': round(r2, 4),
                    'rmse': round(rmse, 4),
                    'akurasi': f"{round(r2 * 100, 2)}%"
                })
            except Exception as e:
                print(f"Error predicting {kelompok_umur}: {e}")
        
        # Sort by age group order
        age_order = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75+']
        predictions_ordered = []
        for age in age_order:
            for pred in predictions:
                if pred['kelompok_umur'] == age:
                    predictions_ordered.append(pred)
                    break
        
        return predictions_ordered if predictions_ordered else predictions
        
    except Exception as e:
        print(f"Error in age group prediction: {e}")
        return []

# ================= INSIGHT - PREDIKSI KELOMPOK UMUR =================
@app.route('/insight')
def insight():
    predictions = predict_age_group_population()
    
    if not predictions:
        return render_template('insight.html', predictions=[])
    
    return render_template('insight.html', predictions=predictions)

# ================= RUN =================
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)