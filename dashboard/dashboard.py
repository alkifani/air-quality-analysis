import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Load data
file_data = 'data/all_data.csv'
data = pd.read_csv(file_data, parse_dates=['datetime'])

# Preprocessing
data['tahun'] = data['datetime'].dt.year
data['bulan'] = data['datetime'].dt.month
data['musim_kode'] = data['bulan'] % 12 // 3 + 1
kode_musim = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Autumn'}
data['musim'] = data['musim_kode'].map(kode_musim)

st.title('📊 Dashboard Analisis Polusi Udara')

st.sidebar.header("Navigasi")
pilihan_menu = st.sidebar.radio("Pilih Analisis", [
    "Visualisasi Berdasarkan Tanggal",
    "Trend PM2.5 Tahunan",
    "Polusi Bulanan/Musiman",
    "Korelasi Suhu & Polutan",
    "Pengaruh Angin",
])

# 0. Visualisasi Berdasarkan Tanggal
if pilihan_menu == "Visualisasi Berdasarkan Tanggal":
    st.header("📆 Visualisasi Data Berdasarkan Rentang Tanggal")
    data['datetime'] = pd.to_datetime(data['datetime'])

    tanggal_mulai = st.sidebar.date_input("Tanggal Mulai", data['datetime'].min().date())
    tanggal_akhir = st.sidebar.date_input("Tanggal Akhir", data['datetime'].max().date())

    if tanggal_mulai > tanggal_akhir:
        st.error("Tanggal mulai tidak boleh lebih besar dari tanggal akhir.")
    else:
        filter_tanggal = (data['datetime'].dt.date >= tanggal_mulai) & (data['datetime'].dt.date <= tanggal_akhir)
        data_terfilter = data.loc[filter_tanggal]

        if data_terfilter.empty:
            st.warning("Tidak ada data pada rentang tanggal yang dipilih.")
        else:
            st.subheader(f"Data dari {tanggal_mulai} hingga {tanggal_akhir}")

            parameter = ['PM2.5 (Partikulat halus)', 'PM10 (Partikulat kasar)',
                         'NO2 (Nitrogen dioksida)', 'SO2 (Sulfur dioksida)',
                         'O3 (Ozon)', 'CO (Karbon monoksida)', 'TEMP (Suhu udara)']
            pilihan_parameter = st.multiselect("Pilih parameter yang ingin divisualisasikan:", parameter, default=['PM2.5 (Partikulat halus)'])

            if pilihan_parameter:
                grafik = px.line(data_terfilter, x='datetime', y=pilihan_parameter, title="Grafik Tren Berdasarkan Tanggal")
                st.plotly_chart(grafik)
            else:
                st.info("Pilih minimal satu parameter untuk divisualisasikan.")

            with st.expander("🔍 Lihat data mentah"):
                st.dataframe(data_terfilter)

# 1. Trend PM2.5 Tahunan
elif pilihan_menu == "Trend PM2.5 Tahunan":
    st.header("📈 Apakah PM2.5 meningkat atau menurun tiap tahun?")
    rata_pm25_tahunan = data.groupby('tahun')['PM2.5 (Partikulat halus)'].mean()
    fig = px.line(rata_pm25_tahunan, x=rata_pm25_tahunan.index, y=rata_pm25_tahunan.values,
                  labels={"x": "Tahun", "y": "Rata-rata PM2.5"},
                  title="Tren Rata-rata PM2.5 per Tahun")
    st.plotly_chart(fig)

# 2. Polusi Bulanan/Musiman
elif pilihan_menu == "Polusi Bulanan/Musiman":
    st.header("📅 Kapan PM2.5 tertinggi dalam setahun?")

    rata_bulanan = data.groupby('bulan')['PM2.5 (Partikulat halus)'].mean()
    fig1 = px.bar(x=rata_bulanan.index, y=rata_bulanan.values,
                  labels={"x": "Bulan", "y": "Rata-rata PM2.5"},
                  title="Rata-rata PM2.5 per Bulan")
    st.plotly_chart(fig1)

    rata_musiman = data.groupby('musim')['PM2.5 (Partikulat halus)'].mean().reindex(['Winter', 'Spring', 'Summer', 'Autumn'])
    fig2 = px.bar(x=rata_musiman.index, y=rata_musiman.values,
                  labels={"x": "Musim", "y": "Rata-rata PM2.5"},
                  title="Rata-rata PM2.5 per Musim")
    st.plotly_chart(fig2)

# 3. Korelasi Suhu dan Polutan
elif pilihan_menu == "Korelasi Suhu & Polutan":
    st.header("🌡️ Korelasi antara suhu dan kadar polutan utama")
    kolom_numerik = ['TEMP (Suhu udara)', 'PM2.5 (Partikulat halus)', 'PM10 (Partikulat kasar)', 'NO2 (Nitrogen dioksida)', 'SO2 (Sulfur dioksida)', 'O3 (Ozon)', 'CO (Karbon monoksida)']
    korelasi = data[kolom_numerik].corr()
    fig, ax = plt.subplots()
    sns.heatmap(korelasi, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
    st.markdown("""
### ℹ️ **Keterangan Polutan:**
Berikut adalah penjelasan singkat tentang masing-masing polutan yang diamati:
- **PM2.5:** Partikel sangat halus dari pembakaran kendaraan & industri.
- **PM10:** Partikel lebih besar yang bisa menyebabkan iritasi saluran pernapasan.
- **SO2:** Gas dari pembakaran bahan bakar fosil, pemicu iritasi pernapasan.
- **NO2:** Gas beracun dari kendaraan & industri.
- **CO:** Gas tak berwarna/berbau dari pembakaran tidak sempurna.
- **O3:** Ozon permukaan bumi dari reaksi polutan & sinar matahari.
""")

# 4. Pengaruh Angin
elif pilihan_menu == "Pengaruh Angin":
    st.header("🌬️ Pengaruh arah dan kecepatan angin terhadap polusi")
    fig1 = px.scatter(data, x='WSPM (Kecepatan angin)', y='PM2.5 (Partikulat halus)', color='wd (Arah angin)',
                      title="Wind Speed vs PM2.5 (warna: arah angin)",
                      labels={"WSPM (Kecepatan angin)": "Kecepatan Angin", "PM2.5 (Partikulat halus)": "PM2.5"})
    st.plotly_chart(fig1)

    st.subheader("📦 Distribusi PM2.5 Berdasarkan Arah Angin")
    fig2, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x="wd (Arah angin)", y="PM2.5 (Partikulat halus)", data=data, ax=ax)
    ax.set_title("Distribusi PM2.5 Berdasarkan Arah Angin")
    ax.set_xlabel("Arah Angin")
    ax.set_ylabel("Konsentrasi PM2.5 (µg/m³)")
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig2)
    st.markdown("""
    Kesimpulan:
1. Pengaruh Kecepatan Angin terhadap PM2.5:
    - Polusi menurun saat kecepatan angin meningkat.
    Terlihat pola negatif (menurun): semakin tinggi kecepatan angin, semakin rendah konsentrasi PM2.5.

    - Korelasi negatif ini masuk akal karena angin dapat menyebarkan polutan di atmosfer, sehingga mengurangi konsentrasinya di satu titik pengukuran.

2. Pengaruh Arah Angin terhadap PM2.5:
    - Dari boxplot terlihat bahwa arah angin dari timur dan timur laut (E, ENE, NE) cenderung menunjukkan konsentrasi PM2.5 lebih tinggi dibandingkan arah lain.

    - Arah angin tertentu mungkin membawa polutan dari wilayah yang lebih tercemar (misalnya kawasan industri, lalu lintas padat, atau daerah padat penduduk).
""")
