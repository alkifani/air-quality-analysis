import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk memuat semua file CSV dalam folder
@st.cache_data
def load_data(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    data_frames = []
    for f in csv_files:
        df = pd.read_csv(os.path.join(folder_path, f))
        df['station'] = f.replace('.csv', '')  # tambahkan nama stasiun
        data_frames.append(df)
    return pd.concat(data_frames, ignore_index=True)

# Load data
folder = "dashboard/data"
df = load_data(folder)

# Gabungkan kolom waktu
df["date"] = pd.to_datetime(df[['year', 'month', 'day']])
df = df.sort_values("date")

# Sidebar filter
st.sidebar.header("Filter Data")
station = st.sidebar.selectbox("Pilih Stasiun", df["station"].unique())
filtered_df = df[df["station"] == station]

# Filter tanggal
min_date = filtered_df["date"].min()
max_date = filtered_df["date"].max()
date_range = st.sidebar.date_input("Rentang Tanggal", [min_date, max_date])
filtered_df = filtered_df[(filtered_df["date"] >= pd.to_datetime(date_range[0])) & (filtered_df["date"] <= pd.to_datetime(date_range[1]))]

# Judul
st.title("📊 Dashboard Kualitas Udara di Beijing")
st.markdown(f"### Data dari Stasiun: `{station}`")

# Tampilkan data
st.dataframe(filtered_df.head(10))

# Visualisasi garis tren PM2.5
st.subheader("🫧 Tren Harian PM2.5")
fig, ax = plt.subplots()
sns.lineplot(data=filtered_df, x="date", y="PM2.5", ax=ax)
ax.set_title("Tren Harian PM2.5")
ax.set_ylabel("Konsentrasi PM2.5")
ax.set_xlabel("Tanggal")
st.pyplot(fig)

# Korelasi antar polutan
st.subheader("🔥 Korelasi antar Polutan")
fig2, ax2 = plt.subplots()
pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
sns.heatmap(filtered_df[pollutants].corr(), annot=True, cmap="coolwarm", ax=ax2)
st.pyplot(fig2)

# Keterangan polutan
st.markdown("""
### ℹ️ **Keterangan Polutan:**
Berikut adalah penjelasan singkat tentang masing-masing polutan yang diamati:
- **PM2.5 (Particulate Matter ≤ 2.5 µm):** Partikel sangat halus yang bisa masuk ke paru-paru dan aliran darah. Sering berasal dari pembakaran kendaraan, industri, dan asap.
- **PM10 (Particulate Matter ≤ 10 µm):** Partikel sedikit lebih besar dari PM2.5, bisa menyebabkan iritasi hidung, tenggorokan, dan pernapasan.
- **SO2 (Sulfur Dioksida):** Gas yang berasal dari pembakaran bahan bakar fosil (batubara dan minyak). Dapat menyebabkan iritasi saluran pernapasan dan memicu asma.
- **NO2 (Nitrogen Dioksida):** Gas berwarna coklat kemerahan yang berasal dari kendaraan bermotor dan pembakaran industri. Berbahaya bagi paru-paru.
- **CO (Karbon Monoksida):** Gas tidak berwarna dan tidak berbau yang sangat beracun. Dihasilkan oleh pembakaran tidak sempurna.
- **O3 (Ozon):** Ozon di permukaan bumi dapat membahayakan sistem pernapasan. Terbentuk dari reaksi kimia antara polutan lain saat terkena sinar matahari.
""")

# Histogram polutan
st.subheader("📊 Histogram Distribusi Polutan")
pollutant_select = st.selectbox("Pilih Polutan", pollutants)
fig3, ax3 = plt.subplots()
sns.histplot(filtered_df[pollutant_select], kde=True, bins=30, ax=ax3)
ax3.set_title(f"Distribusi {pollutant_select}")
st.pyplot(fig3)

# Boxplot per polutan
st.subheader("📦 Boxplot Polutan")
fig4, ax4 = plt.subplots()
sns.boxplot(data=filtered_df[pollutants], ax=ax4)
ax4.set_title("Boxplot Polutan (Deteksi Outlier)")
st.pyplot(fig4)

# Rata-rata bulanan
st.subheader("📅 Rata-rata Bulanan PM2.5")
monthly_avg = filtered_df.groupby(filtered_df["date"].dt.month)["PM2.5"].mean()
fig5, ax5 = plt.subplots()
monthly_avg.plot(kind='bar', ax=ax5)
ax5.set_title("Rata-rata PM2.5 per Bulan")
ax5.set_xlabel("Bulan")
ax5.set_ylabel("PM2.5")
st.pyplot(fig5)

