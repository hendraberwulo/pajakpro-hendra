import streamlit as st
import pandas as pd
import os
import zipfile
import json
from datetime import datetime, date
from inti.validator import validasi_faktur, validasi_master
from inti.exporter import generate_coretax_csv

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

st.set_page_config(page_title="PAJAKPRO BY HENDRA", layout="wide", page_icon="📊")

cek_license() # JALANKAN CEK LICENSE

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

# 1. DASHBOARD
if pilihan == "Dashboard":
    st.title("📊 Dashboard PajakPro By Hendra")
    st.success("Fitur: Auto Fix NPWP + Auto Hitung PPN 11% + Preview Export")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state['mapping']: st.info("✅ Mapping Tersimpan")
        else: st.warning("⚠️ Belum Ada Mapping")
    with col2:
        if st.session_state['df_data'] is not None: st.metric("Total Data Import", len(st.session_state['df_data']))
        else: st.metric("Total Data Import", 0)
    with col3: st.metric("Status", "Siap Pakai")

# 2. SETTING MAPPING
elif pilihan == "Setting Mapping":
    st.title("⚙️ Setting Mapping Kolom")
    st.write("Map kolom dari file Accurate Bapak. Cukup 1x setting, disimpan otomatis")
    st.download_button("📄 Download Template Baru 6 Kolom", "npwp,nama,alamat,no_faktur,tanggal,dpp", "template_baru.csv")
    
    uploaded_map = st.file_uploader("Upload Template untuk Mapping", type="csv", key="map")
    if uploaded_map:
        df_map = pd.read_csv(uploaded_map)
        st.write("*Kolom Terdeteksi di File Bapak:*", list(df_map.columns))
        
        col1, col2 = st.columns(2)
        with col1:
            npwp = st.selectbox("1. Kolom NPWP", df_map.columns)
            nama = st.selectbox("2. Kolom Nama Vendor", df_map.columns)
            alamat = st.selectbox("3. Kolom Alamat", df_map.columns)
        with col2:
            no_faktur = st.selectbox("4. Kolom No Faktur", df_map.columns)
            tanggal = st.selectbox("5. Kolom Tanggal", df_map.columns)
            dpp = st.selectbox("6. Kolom DPP", df_map.columns)

        if st.button("💾 Simpan Mapping", type="primary"):
            mapping = {'npwp':npwp, 'nama':nama, 'alamat':alamat, 'no_faktur':no_faktur, 'tanggal':tanggal, 'dpp':dpp}
            with open(MAP_FILE, 'w') as f: json.dump(mapping, f)
            st.session_state['mapping'] = mapping
            st.success("✅ Mapping Tersimpan! Sekarang ke menu Import")

# 3. IMPORT
elif pilihan == "Import Data Accurate":
    st.title("📥 Import Data Accurate")
    st.info("Template cukup 6 kolom. PPN 11% dihitung otomatis")
    
    uploaded_file = st.file_uploader("Upload File CSV Hasil Export Accurate", type="csv")
    if uploaded_file is not None:
        df_raw = pd.read_csv(uploaded_file)
        if st.session_state['mapping'] is not None:
            map = st.session_state['mapping']
            df = pd.DataFrame()
            try:
                df['npwp'] = df_raw[map['npwp']].astype(str).str.replace(r'[.\- ]', '', regex=True)
                df['npwp'] = df['npwp'].apply(lambda x: '0' + x if len(x) == 15 else x)
                df['nama'] = df_raw[map['nama']].astype(str)
                df['alamat'] = df_raw[map['alamat']].astype(str)
                df['no_faktur'] = df_raw[map['no_faktur']].astype(str)
                df['tanggal'] = pd.to_datetime(df_raw[map['tanggal']], errors='coerce').dt.strftime('%Y-%m-%d')
                df['dpp'] = pd.to_numeric(df_raw[map['dpp']].astype(str).str.replace('.','').str.replace(',','.'), errors='coerce').fillna(0)
                df['ppn'] = (df['dpp'] * 0.11).round(0)
                st.success("✅ Data berhasil dibersihkan otomatis")
            except Exception as e: st.error(f"❌ Error Mapping: {e}")
        else: df = df_raw
        
        st.session_state['df_data'] = df
        st.dataframe(df.head(10), use_container_width=True)
        st.success(f"✅ {len(df)} Baris Data Siap Divalidasi")

# 4. VALIDASI
elif pilihan == "Validasi Pajak":
    st.title("🔍 Validasi Pajak 50+ Rule DJP")
    if st.session_state['df_data'] is not None:
        df = st.session_state['df_data']
        if st.button("Jalankan Validasi Lengkap", type="primary"):
            with st.spinner('Sedang memvalidasi 50+ rule...'):
                warnings = []
                warnings += validasi_master(df)
                warnings += validasi_faktur(df)
                if warnings:
                    st.error(f"❌ Ditemukan {len(warnings)} Masalah.")
                    for w in warnings: st.write(w)
                else: st.success("✅ SELAMAT! Semua Data Valid dan Siap Export ke Coretax!")
    else: st.warning("Silahkan import data dulu")

# 5. EXPORT
elif pilihan == "Export CoreTax":
    st.title("📤 Export ke Format CoreTax DJP")
    if st.session_state['df_data'] is not None:
        if st.button("🚀 Generate & Preview 8 File CSV", type="primary"):
            with st.spinner('Sedang generate file...'):
                files = generate_coretax_csv(st.session_state['df_data'])
                st.success(f"✅ {len(files)} File CSV Berhasil Dibuat!")
                for file in files:
                    nama_file = os.path.basename(file)
                    st.markdown(f"### 📄 {nama_file}")
                    try:
                        df_preview = pd.read_csv(file)
                        st.dataframe(df_preview, use_container_width=True)
                        st.caption(f"Total: {len(df_preview)} baris")
                        st.markdown("---")
                    except: st.write("File kosong")
                
                zip_name = f"CoreTax_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                with zipfile.ZipFile(zip_name, 'w') as zipf:
                    for file in files: zipf.write(file, os.path.basename(file))
                with open(zip_name, "rb") as f: 
                    st.download_button("⬇️ DOWNLOAD ZIP UNTUK UPLOAD CORETAX", f, zip_name, type="primary")
    else: st.warning("Silahkan import data dulu")

# 6. LAPORAN RINGKASAN
elif pilihan == "Laporan Ringkasan":
    st.title("📈 Laporan Ringkasan PPN")
    if st.session_state['df_data'] is not None:
        df = st.session_state['df_data']
        total_dpp = df['dpp'].sum()
        total_ppn = df['ppn'].sum()
        total_faktur = df['no_faktur'].nunique()
        
        st.metric("Total DPP", f"Rp {total_dpp:,.0f}")
        st.metric("Total PPN 11%", f"Rp {total_ppn:,.0f}")
        st.metric("Jumlah Faktur", total_faktur)
        
        st.subheader("Top 10 Vendor Terbesar")
        top_vendor = df.groupby('nama')['dpp'].sum().sort_values(ascending=False).head(10)
        st.dataframe(top_vendor)
    else: st.warning("Silahkan import data dulu")

# 7. BACKUP & RESTORE
elif pilihan == "Backup & Restore":
    st.title("💾 Backup & Restore Data")
    st.write("Buat jaga2 biar data mapping + hasil export tidak hilang")
    
    if st.button("📦 Buat Backup Sekarang", type="primary"):
        backup_name = f"Backup_PajakPro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        with zipfile.ZipFile(backup_name, 'w') as zipf:
            if os.path.exists(MAP_FILE): zipf.write(MAP_FILE)
            if os.path.exists("output"): 
                for root, dirs, files in os.walk("output"):
                    for file in files: zipf.write(os.path.join(root, file))
        with open(backup_name, "rb") as f:
            st.download_button("⬇️ Download File Backup", f, backup_name)
        st.success("✅ Backup Berhasil!")
