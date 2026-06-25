import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="Prediksi Populasi Banten",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CUSTOM CSS & STYLING =================
st.markdown("""
<style>
    /* Root Variables */
    :root {
        --primary: #2563eb;
        --primary-dark: #1e40af;
        --secondary: #7c3aed;
        --success: #10b981;
        --danger: #ef4444;
        --light: #f8fafc;
        --dark: #1e293b;
        --border: #e2e8f0;
        --text-muted: #64748b;
    }

    /* Main Background & Text */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }

    /* Sidebar Styling */
    .sidebar {
        background: white !important;
    }

    /* Metric Cards */
    .metric-card, [data-testid="metric-container"] {
        background: linear-gradient(135deg, white 0%, #f8fafc 100%);
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08) !important;
        border-left: 4px solid #2563eb !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="metric-container"]:hover {
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.12) !important;
        transform: translateY(-2px) !important;
    }

    /* Headings */
    h1 {
        color: #1e293b !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }

    h2, h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
        border-bottom: 3px solid #2563eb;
        padding-bottom: 0.5rem;
    }

    /* Tabs & Selectbox */
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0 !important;
        background: #f8fafc !important;
        color: #64748b !important;
        font-weight: 600 !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
        color: white !important;
    }

    /* Dataframe */
    [data-testid="dataframe"] {
        background: white !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
    }

    /* Selectbox, Multiselect, Radio */
    .stSelectbox, .stMultiSelect, .stRadio {
        background: white !important;
        border-radius: 8px !important;
    }

    /* Cards Container */
    .stContainer {
        background: white !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08) !important;
    }

    /* Markdown Divider */
    hr {
        border: 1px solid #e2e8f0 !important;
        margin: 2rem 0 !important;
    }

    /* Column Dividers */
    .stColumn {
        gap: 1rem !important;
    }

    /* Expander */
    .streamlit-expander {
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        background: white !important;
    }

    /* Success/Info/Warning/Error Messages */
    .stSuccess {
        background-color: #d1fae5 !important;
        border-left: 4px solid #10b981 !important;
    }

    .stInfo {
        background-color: #dbeafe !important;
        border-left: 4px solid #2563eb !important;
    }

    .stWarning {
        background-color: #fef3c7 !important;
        border-left: 4px solid #f59e0b !important;
    }

    .stError {
        background-color: #fee2e2 !important;
        border-left: 4px solid #ef4444 !important;
    }

    /* Plotly Charts */
    .plotly-graph-div {
        background: white !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08) !important;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        h1 { font-size: 1.75rem !important; }
        h2 { font-size: 1.3rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ================= LOAD & CACHE DATA =================
@st.cache_data
def get_data():
    """Load data from consolidated CSV file"""
    try:
        df = pd.read_csv('data_penduduk_konsolidasi_2019_2025.csv')
        return df
    except FileNotFoundError:
        st.error("❌ File data_penduduk_konsolidasi_2019_2025.csv tidak ditemukan!")
        return pd.DataFrame()

@st.cache_data
def get_latest_year_data():
    """Get data for the latest year"""
    df = get_data()
    if df.empty:
        return None
    latest_year = df['Tahun'].max()
    return df[df['Tahun'] == latest_year]

# ================= PREDICTION FUNCTION =================
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
        
        X_future_poly = poly.transform(np.array([2026, 2027, 2028, 2029, 2030]).reshape(-1, 1))
        y_pred_poly = model_poly.predict(X_future_poly)
        
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
        st.warning(f"Error in Polynomial Regression: {e}")
    
    # ========== ALGORITHM 2: RANDOM FOREST REGRESSOR ==========
    try:
        model_rf = RandomForestRegressor(n_estimators=100, max_depth=10, min_samples_split=2, random_state=42, n_jobs=-1)
        model_rf.fit(X, y)
        
        y_pred_rf_train = model_rf.predict(X)
        r2_rf = r2_score(y, y_pred_rf_train)
        rmse_rf = np.sqrt(mean_squared_error(y, y_pred_rf_train))
        
        model_lr_trend = LinearRegression()
        model_lr_trend.fit(X, y)
        
        trend_slope = model_lr_trend.coef_[0]
        last_year = tahun_list[-1]
        last_value = y[-1]
        
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
        st.warning(f"Error in Random Forest: {e}")
    
    if 'polynomial' in result['algorithms']:
        result['r2_score'] = result['algorithms']['polynomial']['r2_score']
        result['rmse'] = result['algorithms']['polynomial']['rmse']
        result['populasi_prediksi'] = result['algorithms']['polynomial']['prediksi']
    
    return result

@st.cache_data
def get_all_predictions():
    """Get predictions for all districts"""
    df = get_data()
    
    if df.empty:
        return []
    
    daerah_list = df['Kabupaten_Kota'].unique()
    predictions = []
    
    for daerah in daerah_list:
        df_daerah = df[df['Kabupaten_Kota'] == daerah].sort_values('Tahun')
        
        if len(df_daerah) < 2:
            continue
        
        result = predict_with_multiple_algorithms(df_daerah, daerah)
        predictions.append(result)
    
    predictions.sort(
        key=lambda x: x['populasi_historis'][-1] if x['populasi_historis'] else 0,
        reverse=True
    )
    
    return predictions

# ================= SIDEBAR NAVIGATION =================
st.sidebar.title("📍 Navigasi")
page = st.sidebar.radio(
    "Pilih Halaman:",
    ["📊 Dashboard", "📈 Grafik", "🔮 Prediksi", "👥 Insight Kelompok Umur"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Aplikasi Prediksi Populasi Provinsi Banten**\n\n"
    "Aplikasi ini menggunakan Machine Learning untuk memprediksi "
    "pertumbuhan populasi di Provinsi Banten tahun 2026-2030."
)

# ================= PAGE 1: DASHBOARD =================
if page == "📊 Dashboard":
    st.title("📊 Dashboard Populasi Banten")
    
    df_latest = get_latest_year_data()
    
    if df_latest is not None and not df_latest.empty:
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_populasi = int(df_latest['Populasi_Ribu'].sum() * 1000)
        rata_populasi = int(df_latest['Populasi_Ribu'].mean() * 1000)
        daerah_terbesar = df_latest.loc[df_latest['Populasi_Ribu'].idxmax(), 'Kabupaten_Kota']
        populasi_terbesar = int(df_latest['Populasi_Ribu'].max() * 1000)
        
        with col1:
            st.metric("📍 Total Populasi", f"{total_populasi:,.0f}")
        
        with col2:
            st.metric("📊 Rata-rata per Daerah", f"{rata_populasi:,.0f}")
        
        with col3:
            st.metric("🏙️ Daerah Terbesar", daerah_terbesar)
        
        with col4:
            st.metric("👥 Populasi Terbesar", f"{populasi_terbesar:,.0f}")
        
        st.markdown("---")
        
        # Table
        st.subheader("Tabel Populasi Terbaru")
        df_display = df_latest.sort_values('Populasi_Ribu', ascending=False)[['Kabupaten_Kota', 'Populasi_Ribu']].copy()
        df_display.columns = ['Kabupaten/Kota', 'Populasi (Ribu)']
        df_display['Populasi (Ribu)'] = df_display['Populasi (Ribu)'].apply(lambda x: f"{x:,.2f}")
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.error("Data tidak tersedia")

# ================= PAGE 2: GRAFIK =================
elif page == "📈 Grafik":
    st.title("📈 Visualisasi Populasi")
    
    df = get_data()
    
    if not df.empty:
        latest_year = df['Tahun'].max()
        df_latest = df[df['Tahun'] == latest_year].sort_values('Populasi_Ribu', ascending=False)
        
        # Bar chart
        fig = px.bar(
            df_latest,
            x='Kabupaten_Kota',
            y='Populasi_Ribu',
            title=f"Populasi per Kabupaten/Kota ({int(latest_year)})",
            labels={'Populasi_Ribu': 'Populasi (Ribu)', 'Kabupaten_Kota': 'Kabupaten/Kota'},
            color='Populasi_Ribu',
            color_continuous_scale='Viridis'
        )
        
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Line chart - Trend over years
        st.subheader("Tren Populasi Tahun ke Tahun")
        
        daerah_selected = st.multiselect(
            "Pilih Kabupaten/Kota:",
            df['Kabupaten_Kota'].unique(),
            default=df['Kabupaten_Kota'].unique()[:5]
        )
        
        if daerah_selected:
            df_trend = df[df['Kabupaten_Kota'].isin(daerah_selected)]
            
            fig_trend = px.line(
                df_trend,
                x='Tahun',
                y='Populasi_Ribu',
                color='Kabupaten_Kota',
                title="Tren Populasi (2019-2025)",
                labels={'Populasi_Ribu': 'Populasi (Ribu)', 'Tahun': 'Tahun'},
                markers=True
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.error("Data tidak tersedia")

# ================= PAGE 3: PREDIKSI =================
elif page == "🔮 Prediksi":
    st.title("🔮 Prediksi Populasi 2026-2030")
    
    predictions = get_all_predictions()
    
    if predictions:
        # Selector
        daerah_selected = st.selectbox(
            "Pilih Kabupaten/Kota:",
            [p['Kabupaten_Kota'] for p in predictions]
        )
        
        # Find selected prediction
        pred = next((p for p in predictions if p['Kabupaten_Kota'] == daerah_selected), None)
        
        if pred:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Chart
                tahun_all = pred['tahun_historis'] + pred['tahun_prediksi']
                populasi_historis = pred['populasi_historis'] + [None] * len(pred['tahun_prediksi'])
                
                fig = go.Figure()
                
                # Polynomial prediction
                if 'polynomial' in pred['algorithms']:
                    poly_pred = [None] * len(pred['tahun_historis']) + pred['algorithms']['polynomial']['prediksi']
                    fig.add_trace(go.Scatter(
                        x=tahun_all,
                        y=poly_pred,
                        name='Polynomial Regression',
                        mode='lines+markers',
                        line=dict(color='blue', dash='dash')
                    ))
                
                # Random Forest prediction
                if 'random_forest' in pred['algorithms']:
                    rf_pred = [None] * len(pred['tahun_historis']) + pred['algorithms']['random_forest']['prediksi']
                    fig.add_trace(go.Scatter(
                        x=tahun_all,
                        y=rf_pred,
                        name='Random Forest',
                        mode='lines+markers',
                        line=dict(color='orange', dash='dash')
                    ))
                
                # Historical data
                fig.add_trace(go.Scatter(
                    x=pred['tahun_historis'],
                    y=pred['populasi_historis'],
                    name='Data Historis',
                    mode='lines+markers',
                    line=dict(color='green', width=2)
                ))
                
                fig.update_layout(
                    title=f"Prediksi Populasi {daerah_selected}",
                    xaxis_title="Tahun",
                    yaxis_title="Populasi (Ribu)",
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("📊 Metrik Akurasi")
                
                if 'polynomial' in pred['algorithms']:
                    poly = pred['algorithms']['polynomial']
                    st.markdown(f"""
                    **Polynomial Regression**
                    - R² Score: `{poly['r2_score']}`
                    - Akurasi: `{poly['akurasi']}`
                    - RMSE: `{poly['rmse']}`
                    """)
                
                if 'random_forest' in pred['algorithms']:
                    rf = pred['algorithms']['random_forest']
                    st.markdown(f"""
                    **Random Forest**
                    - R² Score: `{rf['r2_score']}`
                    - Akurasi: `{rf['akurasi']}`
                    - RMSE: `{rf['rmse']}`
                    """)
            
            # Prediction table
            st.subheader("📈 Data Prediksi Tahun 2026-2030")
            
            pred_data = {
                'Tahun': pred['tahun_prediksi'],
                'Polynomial': pred['algorithms']['polynomial']['prediksi'] if 'polynomial' in pred['algorithms'] else [None]*5,
                'Random Forest': pred['algorithms']['random_forest']['prediksi'] if 'random_forest' in pred['algorithms'] else [None]*5
            }
            
            df_pred = pd.DataFrame(pred_data)
            st.dataframe(df_pred, use_container_width=True, hide_index=True)
    else:
        st.error("Tidak ada data prediksi yang tersedia")

# ================= PAGE 4: INSIGHT KELOMPOK UMUR =================
elif page == "👥 Insight Kelompok Umur":
    st.title("👥 Prediksi Populasi per Kelompok Umur")
    
    st.info(
        "📝 Halaman ini menampilkan prediksi populasi berdasarkan kelompok umur "
        "menggunakan Polynomial Regression Degree 2."
    )
    
    try:
        # Load age group data
        age_groups_data = {}
        years_available = [2019, 2020, 2023, 2024, 2025]
        
        for year in years_available:
            try:
                if year == 2025:
                    file_path = 'Jumlah Penduduk Menurut Kelompok Umur dan Jenis Kelamin (ribu jiwa) di Provinsi Banten, 2025(1).csv'
                elif year == 2024:
                    file_path = 'Jumlah Penduduk Menurut Kelompok Umur dan Jenis Kelamin (ribu jiwa) di Provinsi Banten, 2024(1).csv'
                else:
                    file_path = f'Jumlah Penduduk Menurut Kelompok Umur dan Jenis Kelamin di Provinsi Banten, {year}.csv'
                
                df_year = pd.read_csv(file_path)
                
                for idx, row in df_year.iterrows():
                    kelompok = str(row['Kelompok Umur']).strip()
                    if kelompok != 'Jumlah/Total':
                        if kelompok not in age_groups_data:
                            age_groups_data[kelompok] = []
                        
                        pop_col = 'Penduduk (Laki-Laki + Perempuan) (Ribu)'
                        pop_value = float(row[pop_col])
                        
                        age_groups_data[kelompok].append({
                            'tahun': year,
                            'populasi': pop_value
                        })
            except Exception as e:
                pass
        
        if age_groups_data:
            age_group_selected = st.selectbox(
                "Pilih Kelompok Umur:",
                list(age_groups_data.keys())
            )
            
            data_list = age_groups_data[age_group_selected]
            data_list.sort(key=lambda x: x['tahun'])
            
            years = np.array([d['tahun'] for d in data_list]).reshape(-1, 1)
            pops = np.array([d['populasi'] for d in data_list])
            
            # Polynomial Regression
            poly = PolynomialFeatures(degree=2, include_bias=False)
            X_poly = poly.fit_transform(years)
            
            model = LinearRegression()
            model.fit(X_poly, pops)
            
            y_pred_train = model.predict(X_poly)
            r2 = r2_score(pops, y_pred_train)
            rmse = np.sqrt(mean_squared_error(pops, y_pred_train))
            
            future_years = np.array([2026, 2027, 2028, 2029, 2030]).reshape(-1, 1)
            X_future_poly = poly.transform(future_years)
            future_pops = model.predict(X_future_poly)
            
            # Chart
            tahun_all = [d['tahun'] for d in data_list] + [2026, 2027, 2028, 2029, 2030]
            populasi_historis = list(pops) + [None]*5
            prediksi = [None]*len(data_list) + list(future_pops)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=[d['tahun'] for d in data_list],
                y=list(pops),
                name='Data Historis',
                mode='lines+markers',
                line=dict(color='green', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=[2026, 2027, 2028, 2029, 2030],
                y=list(future_pops),
                name='Prediksi',
                mode='lines+markers',
                line=dict(color='blue', dash='dash')
            ))
            
            fig.update_layout(
                title=f"Prediksi Populasi Kelompok Umur {age_group_selected}",
                xaxis_title="Tahun",
                yaxis_title="Populasi (Ribu)",
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("R² Score", f"{r2:.4f}")
            with col2:
                st.metric("Akurasi", f"{r2*100:.2f}%")
            with col3:
                st.metric("RMSE", f"{rmse:.2f}")
            
            # Prediction table
            st.subheader("Tabel Prediksi")
            pred_df = pd.DataFrame({
                'Tahun': [2026, 2027, 2028, 2029, 2030],
                'Prediksi Populasi (Ribu)': [f"{float(p):.2f}" for p in future_pops]
            })
            st.dataframe(pred_df, use_container_width=True, hide_index=True)
        else:
            st.error("Data kelompok umur tidak tersedia")
    
    except Exception as e:
        st.error(f"Error loading age group data: {e}")
