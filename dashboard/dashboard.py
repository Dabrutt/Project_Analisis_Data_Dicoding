import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load dataset yang diperlukan
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  
data_path = os.path.join(base_path, "data")

# Atur path ke file CSV
path_day = os.path.join(data_path, "day.csv")
path_hour = os.path.join(data_path, "hour.csv")

day_df = pd.read_csv(path_day)
hour_df = pd.read_csv(path_hour)

# Sidebar
st.sidebar.title("Data Pembuat 🧑🏻‍💻")
st.sidebar.write("**Nama:** Muhammad Daffa Eka Pramudita")
st.sidebar.write("**Email:** mdaffa.ekapram@gmail.com")
st.sidebar.write("**ID Dicoding:** dabrut")

st.sidebar.markdown("---")

st.sidebar.title("Filter Data 📊")
selected_season = st.sidebar.selectbox("Pilih Musim:", ["All", "Spring", "Summer", "Fall", "Winter"], index=0)

# Pemetaan musim
season_mapping = {"Spring": 1, "Summer": 2, "Fall": 3, "Winter": 4}

# Filter data berdasarkan pilihan
filtered_day_df = day_df.copy()
if selected_season != "All":
    filtered_day_df = filtered_day_df[filtered_day_df["season"] == season_mapping[selected_season]]
# Dashboard Title
st.title("Dashboard Penyewaan Sepeda🚲")
st.write("""Dashboard ini menyajikan analisis data penyewaan sepeda berdasarkan 
         berbagai faktor seperti waktu, musim, dan suhu udara. 
         Dengan fitur interaktif, Anda dapat mengeksplorasi tren penggunaan sepeda 
         untuk mendapatkan insight yang lebih dalam.""")
# Line Plot - Rata-rata Penggunaan Sepeda Berdasarkan Jam
st.subheader("Rata-rata Penggunaan Sepeda Berdasarkan Jam")
hour_group = hour_df.groupby("hr")["cnt"].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x="hr", y="cnt", data=hour_group, marker="o", color="blue", ax=ax)
ax.set_title("Rata-rata Penggunaan Sepeda Berdasarkan Jam")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewa Sepeda")
ax.set_xticks(range(0, 24))
ax.grid(True)
st.pyplot(fig)

# Bar Plot - Hari Kerja dengan Hari Libur
st.subheader("Rata-rata Penggunaan Sepeda pada Hari Kerja dan Hari Libur")
workingday_group = filtered_day_df.groupby("workingday")["cnt"].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="workingday", y="cnt", hue="workingday", data=workingday_group, palette="Set2", legend=False, ax=ax)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Hari Libur", "Hari Kerja"])
ax.set_title("Rata-rata Penggunaan Sepeda pada Hari Kerja vs. Hari Libur")
ax.set_xlabel("Kategori Hari")
ax.set_ylabel("Rata-rata Penyewa Sepeda")
ax.grid(axis='y')
st.pyplot(fig)

# Bar Plot - Penggunaan Sepeda Berdasarkan Musim (Hanya jika All dipilih)
if selected_season == "All":
    st.subheader("Rata-rata Penggunaan Sepeda Berdasarkan Musim")
    season_group = day_df.groupby("season")["cnt"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="season", y="cnt", data=season_group, palette="Set2", legend=False, ax=ax)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
    ax.set_title("Rata-rata Penggunaan Sepeda Berdasarkan Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewa Sepeda")
    ax.grid(axis='y')
    st.pyplot(fig)
else:
    st.subheader(f"Rata-rata Penggunaan Sepeda pada Musim {selected_season}")
    season_group = filtered_day_df.groupby("season")["cnt"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="season", y="cnt", data=season_group, palette="Set2", legend=False, ax=ax)
    ax.set_xticks([season_mapping[selected_season]])
    ax.set_xticklabels([selected_season])
    ax.set_title(f"Rata-rata Penggunaan Sepeda pada Musim {selected_season}")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewa Sepeda")
    ax.grid(axis='y')
    st.pyplot(fig)

# Regplot - Hubungan Temperatur dan Jumlah Penyewa Sepeda
st.subheader("Hubungan Temperatur dan Jumlah Penyewa Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.regplot(x="temp", y="cnt", data=filtered_day_df, scatter_kws={"color": "darkcyan", "alpha":0.5}, line_kws={"color": "darkblue"}, ax=ax)
ax.set_title("Hubungan Temperatur dan Jumlah Penyewa Sepeda")
ax.set_xlabel("Temperatur (Normalized)")
ax.set_ylabel("Rata-rata Penyewa Sepeda")
ax.grid(True)
st.pyplot(fig)

# Kesimpulan
st.subheader("Kesimpulan")
st.write("1. Penggunaan sepeda mencapai puncaknya pada sekitar pukul 08.00 dan pukul 17.00, yang bertepatan dengan jam berangkat dan pulang kerja. Dengan begitu, menyesuaikan layanan penyewaan sepeda pada jam sibuk dapat dilakukan untuk mengakomodasi lonjakan pengguna.")
st.write("2. Jumlah rata-rata pengguna sepeda pada hari kerja lebih tinggi daripada hari libur. Sehingga dapat disimpulkan bahwa sepeda digunakan lebih banyak untuk pergi ke kantor/sekolah. Oleh karena itu, mengadakan promosi pada hari libur mungkin dapat meratakan jumlah pengguna sepeda.")
st.write("3. Musim gugur menjadi musim dengan pengguna sepeda tertinggi, yang kemudian menurun setelah memasuki musim dingin. Hal ini mungkin berkaitan dengan suhu udara yang terlalu dingin sehingga mengurangi kenyamanan saat mengendarai sepeda. Oleh karena itu, melakukan maintenance kepada sepeda-sepeda selama musim dingin mungkin menjadi solusi yang baik untuk menghadapi lonjakan pengguna pada musim berikutnya.")
st.write("4. Dapat disimpulkan bahwa kenaikan suhu udara beriringan dengan naiknya pengguna sepeda. Namun, suhu yang terlalu tinggi juga dapat menurunkan angka penggunaan sepeda. Oleh karena itu, mungkin dengan membangun fasilitas pendukung seperti tempat berteduh dapat menjadi solusi, sehingga pengguna dapat beristirahat disaat suhu sedang panas-panasnya.")

st.markdown("---")

# Copyright
st.write("© 2025 Muhammad Daffa Eka Pramudita")
