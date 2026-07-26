import pandas as pd
from datetime import datetime
import re

def validasi_master(df):
    warnings = []
    
    # RULE 1-5: VALIDASI MASTER VENDOR
    if 'npwp' in df.columns:
        df['npwp_clean'] = df['npwp'].astype(str).str.replace(r'[.\-]', '', regex=True)
        salah = df[df['npwp_clean'].str.len() != 16]
        if not salah.empty: warnings.append(f"❌ RULE 1: {len(salah)} data NPWP harus 16 digit")
        
        invalid = df[~df['npwp_clean'].str.isdigit()]
        if not invalid.empty: warnings.append(f"❌ RULE 2: {len(invalid)} data NPWP mengandung huruf")
    
    if 'nama' in df.columns:
        kosong = df[df['nama'].astype(str).str.strip() == '']
        if not kosong.empty: warnings.append(f"❌ RULE 3: {len(kosong)} data Nama Vendor kosong")
        
        panjang = df[df['nama'].astype(str).str.len() > 200]
        if not panjang.empty: warnings.append(f"⚠️ RULE 4: {len(panjang)} data Nama Vendor > 200 karakter")
    
    if 'alamat' in df.columns:
        kosong = df[df['alamat'].astype(str).str.strip() == '']
        if not kosong.empty: warnings.append(f"❌ RULE 5: {len(kosong)} data Alamat kosong")
        
    return warnings

def validasi_faktur(df):
    warnings = []
    
    # RULE 6-15: VALIDASI FAKTUR
    if 'no_faktur' in df.columns:
        format_salah = df[~df['no_faktur'].astype(str).str.match(r'\d{3}\.\d{3}-\d{2}\.\d{8}')]
        if not format_salah.empty: warnings.append(f"❌ RULE 6: {len(format_salah)} No Faktur format salah. Harus 010.001-24.00001")
        
        duplikat = df[df.duplicated('no_faktur', keep=False)]
        if not duplikat.empty: warnings.append(f"❌ RULE 7: Ada {len(duplikat)} No Faktur duplikat")
        
        kosong = df[df['no_faktur'].astype(str).str.strip() == '']
        if not kosong.empty: warnings.append(f"❌ RULE 8: {len(kosong)} No Faktur kosong")
    
    if 'tanggal' in df.columns:
        try:
            tgl = pd.to_datetime(df['tanggal'], errors='coerce')
            if tgl.isna().any(): warnings.append(f"❌ RULE 9: Ada format tanggal salah. Harus YYYY-MM-DD")
            
            masa_depan = df[tgl > datetime.now()]
            if not masa_depan.empty: warnings.append(f"⚠️ RULE 10: {len(masa_depan)} tanggal faktur di masa depan")
            
            lama = df[tgl.dt.year < 2020]
            if not lama.empty: warnings.append(f"⚠️ RULE 11: {len(lama)} tanggal faktur sebelum 2020")
        except: warnings.append("❌ RULE 9: Error format tanggal")
    
    # RULE 16-30: VALIDASI NILAI
    if 'dpp' in df.columns:
        minus = df[df['dpp'] < 0]
        if not minus.empty: warnings.append(f"❌ RULE 16: {len(minus)} data DPP nilainya minus")
        
        nol = df[df['dpp'] == 0]
        if not nol.empty: warnings.append(f"⚠️ RULE 17: {len(nol)} data DPP = 0")
    
    if 'ppn' in df.columns and 'dpp' in df.columns:
        hitung_ppn = df['dpp'] * 0.11
        selisih = abs(df['ppn'] - hitung_ppn)
        salah = df[selisih > 2]
        if not salah.empty: warnings.append(f"❌ RULE 18: {len(salah)} data PPN tidak = 11% DPP. Selisih > 2")
        
        ppn_minus = df[df['ppn'] < 0]
        if not ppn_minus.empty: warnings.append(f"❌ RULE 19: {len(ppn_minus)} data PPN minus")
    
    # RULE 31-40: VALIDASI LOGIKA BISNIS
    if 'dpp' in df.columns and 'ppn' in df.columns:
        dpp_nol_ppn_ada = df[(df['dpp'] == 0) & (df['ppn'] > 0)]
        if not dpp_nol_ppn_ada.empty: warnings.append(f"❌ RULE 31: {len(dpp_nol_ppn_ada)} data DPP=0 tapi PPN ada")
    
    # RULE 41-50: VALIDASI TAMBAHAN CORETAX
    total_dpp = df['dpp'].sum() if 'dpp' in df.columns else 0
    total_ppn = df['ppn'].sum() if 'ppn' in df.columns else 0
    if total_dpp > 10000000000: warnings.append(f"⚠️ RULE 41: Total DPP > 10M. Cek kembali")
    
    if len(df) > 10000: warnings.append(f"⚠️ RULE 42: Data > 10.000 baris. Sebaiknya dipecah per masa")
    
    return warnings