import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title("Dashboard Analisis Data")

# Sidebar untuk navigasi dan kontrol
st.sidebar.header("Laporan Bike Sharing")
pilih_analisis = st.sidebar.radio(
    "Pilih Analisis:",
    ("Pola Aktivitas Per Jam", "Korelasi Antar Variabel")
)
tampil_data = st.sidebar.checkbox("Tampilkan Data Mentah", value=False)
st.sidebar.header("Muhammad Adika Zahran")

# Tab untuk tampilan tambahan (optional)
tab_dashboard, tab_insight = st.tabs(["Dashboard Utama", "Tentang & Insight"])
with tab_insight:
    st.markdown("""
    ### Tentang Dashboard
    Dashboard ini memuat dua analisis:
    
    1. **Pola Aktivitas Per Jam**  
       Menganalisis perbedaan aktivitas antara hari kerja dan akhir pekan (data dari hour.csv).  
       
    2. **Korelasi Antar Variabel**  
       Menampilkan hubungan antar variabel dari data day.csv dan hour.csv untuk membantu strategi bisnis.
    """)

# =====================================================
# Bagian 1: Analisis Pola Aktivitas Per Jam (hour.csv)
# =====================================================
if pilih_analisis == "Pola Aktivitas Per Jam":
    st.header("Pola Aktivitas Per Jam (hour.csv)")
    st.markdown("""
    **Pertanyaan:**  
    Bagaimana pola aktivitas per jam berbeda antara hari kerja dan akhir pekan? Jam berapa yang jadi puncak, dan jam berapa yang paling sepi?
    """)
    
    # Baca data hour.csv
    try:
        hour_df = pd.read_csv("hour.csv")
    except Exception as ex:
        st.error("Gagal membaca file hour.csv: " + str(ex))
        st.stop()
    
    # Ubah kolom tanggal ke datetime bila ada
    if "dteday" in hour_df.columns:
        hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Buat kolom hari dalam minggu dan flag weekend
    hour_df['day_of_week'] = hour_df['dteday'].dt.dayofweek  # 0=Senin, ... 6=Minggu
    hour_df['is_weekend'] = hour_df['day_of_week'] >= 5       # Weekend: Sabtu & Minggu
    
    # Hitung rata-rata aktivitas per jam berdasarkan tipe hari
    summary = hour_df.groupby(['hr', 'is_weekend'])['cnt'].mean().reset_index()
    summary['day_type'] = np.where(summary['is_weekend'], 'Weekend', 'Weekday')
    
    # Plot garis per jam
    fig, ax = plt.subplots(figsize=(10,6))
    sns.lineplot(data=summary, x='hr', y='cnt', hue='day_type', marker='o', ax=ax)
    ax.set_title("Aktivitas Per Jam: Weekday vs. Weekend")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Aktivitas")
    ax.set_xticks(range(0,24))
    st.pyplot(fig)
    
    # Cari peak dan quiet hour dari keseluruhan
    overall = hour_df.groupby("hr")["cnt"].mean()
    peak = overall.idxmax()
    quiet = overall.idxmin()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Peak Hour", f"Jam {peak}")
    with col2:
        st.metric("Quiet Hour", f"Jam {quiet}")
    
    # Tampilkan data mentah jika dicentang
    if tampil_data:
        st.subheader("Data Summary Hourly")
        st.dataframe(summary)

# =====================================================
# Bagian 2: Analisis Korelasi Antar Variabel (day.csv & hour.csv)
# =====================================================
elif pilih_analisis == "Korelasi Antar Variabel":
    st.header("Korelasi Antar Variabel")
    st.markdown("""
    **Pertanyaan:**  
    Bagaimana hubungan antar variabel dalam day.csv dan hour.csv, dan bagaimana korelasi tersebut memberikan insight untuk strategi bisnis?
    """)
    
    # Baca data day.csv
    try:
        day_df = pd.read_csv("day.csv")
    except Exception as ex:
        st.error("Gagal membaca file day.csv: " + str(ex))
        st.stop()
    
    if "dteday" in day_df.columns:
        day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    
    # Hitung dan plot matriks korelasi day.csv
    corr_day = day_df.corr()
    st.subheader("Matriks Korelasi - Data Harian (day.csv)")
    fig_day, ax_day = plt.subplots(figsize=(10,8))
    sns.heatmap(corr_day, annot=True, cmap="coolwarm", fmt=".2f", ax=ax_day)
    st.pyplot(fig_day)
    
    # Baca data hour.csv (untuk korelasi tambahan)
    try:
        hour_df = pd.read_csv("hour.csv")
    except Exception as ex:
        st.error("Gagal membaca file hour.csv: " + str(ex))
        st.stop()
    if "dteday" in hour_df.columns:
        hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    corr_hour = hour_df.corr()
    st.subheader("Matriks Korelasi - Data Jam (hour.csv)")
    fig_hour, ax_hour = plt.subplots(figsize=(10,8))
    sns.heatmap(corr_hour, annot=True, cmap="coolwarm", fmt=".2f", ax=ax_hour)
    st.pyplot(fig_hour)
    
    st.markdown("""
    **Insight:**  
    - Jika variabel seperti suhu (temp) berkorelasi tinggi dengan total aktivitas (cnt) di day.csv, maka cuaca berperan penting dalam permintaan.  
    - Korelasi di data hour.csv membantu menentukan waktu operasional optimal untuk penjadwalan dan pemasaran.
    """)
    
    # Tampilkan matriks korelasi mentah jika dicentang
    if tampil_data:
        st.subheader("Matriks Korelasi Mentah - day.csv")
        st.dataframe(corr_day)
        st.subheader("Matriks Korelasi Mentah - hour.csv")
        st.dataframe(corr_hour)

# Container tambahan (expander) untuk penjelasan lebih lanjut
with st.expander("Lihat Penjelasan Tambahan"):
    st.markdown("""
    **Dashboard Interaktif:**  
    Dashboard ini dirancang untuk mengeksplorasi data Bike Sharing. Gunakan kontrol di sidebar untuk memilih analisis yang ingin dilihat. Data mentah bisa ditampilkan dengan mencentang opsi yang tersedia.
    """)
