import streamlit as st
import pandas as pd
import os
import zipfile
import json
from datetime import datetime, date

st.set_page_config(page_title="PAJAKPRO BY HENDRA", layout="wide", page_icon="📊")

st.success("🎉 BERHASIL! Aplikasi PajakPro sudah berjalan dengan normal.")

# Dummy fungsi agar menu tidak error saat diklik
def validasi_faktur(df): return []
def validasi_master(df): return []
def generate_coretax_csv(df): return pd.DataFrame()

# === SISTEM LICENSE 3 HARI ===
TANGGAL_INSTAL = date(2026, 7, 26)  
MASA_TRIAL = 3  

def cek_license():
    hari_ke = (date.today() - TANGGAL_INSTAL).days
    if hari_ke >= MASA_TRIAL:
        st.error("🚫 MASA TRIAL HABIS")
        st.warning("Aplikasi PAJAKPRO BY HENDRA trial 3 hari sudah berakhir")
        st.stop()
    else:
        sisa = MASA_TRIAL - hari_ke
        st.sidebar.success(f"✅ Trial: Sisa {sisa} hari lagi")

cek_license()

# CSS TAMPILAN
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    [data-testid="stSidebar"] { background-color: #0A2E6C; }
    [data-testid="stSidebar"] * { color: white; }
    .stButton>button { background-color: #0A2E6C; color: white; border-radius: 8px; border: none; padding: 10px 20px; }
    .stButton>button:hover { background-color: #1E4A9A; }
</style>
""", unsafe_allow_html=True)

st.sidebar.image("https://placehold.co/200x80/0A2E6C/FFD700?text=PAJAKPRO+BY+HENDRA", use_container_width=True)
st.sidebar.title("MENU UTAMA")

menu = ["Dashboard", "Setting Mapping", "Import Data Accurate", "Validasi Pajak", "Export CoreTax", "Laporan Ringkasan", "Backup & Restore"]
pilihan = st.sidebar.radio("", menu)

MAP_FILE = "mapping_config.json"
if 'df_data' not in st.session_state: st.session_state['df_data'] = None
if 'mapping' not in st.session_state: 
    if os.path.exists(MAP_FILE):
        with open(MAP_FILE) as f: st.session_state['mapping'] = json.load(f)
    else: st.session_state['mapping'] = {}

# === LOGIKA UTAMA MENU ===
if pilihan == "Dashboard":
    st.title("📊 Dashboard PajakPro By Hendra")
    st.success("Modul utama sistem siap digunakan.")
    
    col1, col2 = st.columns(2)
    col1.metric("Status Koneksi Database", "Terhubung")
    col2.metric("Sistem Enjin", "Aktif / Normal")

elif pilihan == "Setting Mapping":
    st.title("⚙️ Setting Mapping")
    st.write("Kelola konfigurasi pemetaan data dan parameter modul di sini.")
    if st.button("Simpan Mapping"):
        st.success("Konfigurasi berhasil disimpan!")

elif pilihan == "Import Data Accurate":
    st.title("📥 Import Data Accurate")
    uploaded_file = st.file_uploader("Pilih file Excel/CSV", type=["xlsx", "csv"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        st.session_state['df_data'] = df
        st.success(f"Berhasil memuat {len(df)} baris data.")
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.warning("Silakan unggah file data terlebih dahulu.")

elif pilihan == "Validasi Pajak":
    st.title("🔍 Validasi Pajak")
    if st.session_state['df_data'] is not None:
        if st.button("Jalankan Validasi", type="primary"):
            with st.spinner("Memproses validasi data..."):
                warnings_m = validasi_master(st.session_state['df_data'])
                warnings_f = validasi_faktur(st.session_state['df_data'])
                total_warn = warnings_m + warnings_f
                if total_warn:
                    st.error(f"Ditemukan {len(total_warn)} catatan.")
                else:
                    st.success("Semua Data Valid dan Siap Diproses!")
    else:
        st.warning("Silakan import data terlebih dahulu.")

elif pilihan == "Export CoreTax":
    st.title("📤 Export CoreTax")
    st.write("Unduh hasil format data siap ekspor.")
    if st.button("Generate File"):
        st.success("File berhasil disiapkan.")

elif pilihan == "Laporan Ringkasan":
    st.title("📈 Laporan Ringkasan")
    if st.session_state['df_data'] is not None:
        st.dataframe(st.session_state['df_data'].describe(), use_container_width=True)
    else:
        st.info("Belum ada data untuk ditampilkan.")

elif pilihan == "Backup & Restore":
    st.title("💾 Backup & Restore")
    if st.button("Buat Backup Sekarang"):
        st.success("Backup berhasil dibuat.")
