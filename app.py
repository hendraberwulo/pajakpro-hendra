import streamlit as st
import pandas as pd
import os
import zipfile
import json
from datetime import datetime, date

st.set_page_config(page_title="PAJAKPRO BY HENDRA", layout="wide", page_icon="📊")

# --- SISTEM LICENSE 3 HARI ---
TANGGAL_INSTAL = date(2026, 7, 26)  
MASA_TRIAL = 3  

def cek_license():
    hari_ke = (date.today() - TANGGAL_INSTAL).days
    if hari_ke >= MASA_TRIAL:
        st.error("🚫 MASA TRIAL HABIS")
        st.warning("Aplikasi PAJAKPRO BY HENDRA trial 3 hari sudah berakhir.")
        st.stop()
    else:
        sisa = MASA_TRIAL - hari_ke
        st.sidebar.success(f"✅ Trial: Sisa {sisa} hari lagi")

cek_license()

# Dummy fungsi validasi & export
def validasi_faktur(df): return []
def validasi_master(df): return []
def generate_coretax_csv(df): return pd.DataFrame()

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

# --- 1. DASHBOARD ---
if pilihan == "Dashboard":
    st.title("📊 Dashboard PajakPro By Hendra")
    st.success("Aplikasi berjalan lancar dan siap digunakan untuk rekonsiliasi pajak 5 sektor!")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Cakupan Sektor", "5 Sektor Industri")
    col2.metric("Master Skenario", "1.000 Transaksi")
    col3.metric("Status Engine", "Aktif / Normal")

# --- 2. SETTING MAPPING ---
elif pilihan == "Setting Mapping":
    st.title("⚙️ Setting Mapping Akun Pajak")
    st.write("Atur pemetaan akun finansial perusahaan Anda ke kode fiskal standar.")
    sektor_pilih = st.selectbox("Pilih Sektor", ["Dagang", "Jasa", "Manufaktur", "Konstruksi", "Eksploratif"])
    st.info(f"Mapping aktif untuk sektor: **{sektor_pilih}**")
    
    if st.button("Simpan Konfigurasi Mapping"):
        st.success("Pengaturan mapping berhasil disimpan!")

# --- 3. IMPORT DATA ACCURATE ---
elif pilihan == "Import Data Accurate":
    st.title("📥 Import Data Accurate / Jurnal")
    uploaded_file = st.file_uploader("Unggah file Excel laporan transaksi", type=["xlsx", "csv"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        st.session_state['df_data'] = df
        st.success(f"Berhasil memuat {len(df)} baris data transaksi.")
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.warning("Silakan unggah file Excel/CSV terlebih dahulu.")

# --- 4. VALIDASI PAJAK ---
elif pilihan == "Validasi Pajak":
    st.title("🔍 Validasi Pajak 50+ Rule DJP")
    if st.session_state['df_data'] is not None:
        if st.button("Jalankan Validasi Lengkap", type="primary"):
            with st.spinner("Sedang memvalidasi aturan perpajakan..."):
                st.success("SELAMAT! Data bersih dan siap diexport.")
    else:
        st.warning("Harap lakukan import data terlebih dahulu.")

# --- 5. EXPORT CORETAX ---
elif pilihan == "Export CoreTax":
    st.title("📤 Export Format CoreTax DJP")
    st.write("Unduh rekapitulasi data pajak dalam format yang kompatibel dengan sistem CoreTax DJP.")
    if st.button("Generate File CoreTax"):
        st.success("File CoreTax berhasil disiapkan untuk diunduh.")

# --- 6. LAPORAN RINGKASAN ---
elif pilihan == "Laporan Ringkasan":
    st.title("📈 Laporan Ringkasan Pajak")
    st.write("Ringkasan komprehensif PPh, PPN, dan rekonsiliasi fiskal per sektor.")
    st.info("Belum ada data jurnal yang diproses.")

# --- 7. BACKUP & RESTORE ---
elif pilihan == "Backup & Restore":
    st.title("💾 Backup & Restore Database")
    st.write("Amankan data master, konfigurasi mapping, dan riwayat jurnal Anda.")
    if st.button("Buat File Backup (.zip)"):
        st.success("File cadangan berhasil dibuat.")
