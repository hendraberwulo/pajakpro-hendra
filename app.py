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
def generate_coretax_csv(df): return []

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
    else: st.session_state['mapping'] = None

if pilihan == "Dashboard":
    st.title("📊 Dashboard PajakPro By Hendra")
    st.success("Aplikasi berjalan lancar!")
