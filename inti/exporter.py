import pandas as pd
import os
from datetime import datetime

def generate_coretax_csv(df, output_path="output/"):
    os.makedirs(output_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    files_created = []

    # 01. MASTER - Data Vendor
    master = pd.DataFrame()
    if 'npwp' in df.columns: master['NPWP'] = df['npwp']
    if 'nama' in df.columns: master['NAMA'] = df['nama']
    if 'alamat' in df.columns: master['ALAMAT'] = df['alamat']
    master = master.drop_duplicates()
    f1 = f"{output_path}01_Master_{timestamp}.csv"
    master.to_csv(f1, index=False); files_created.append(f1)

    # 02. FAKTUR MASUK
    faktur = pd.DataFrame()
    if 'no_faktur' in df.columns: faktur['NO_FAKTUR'] = df['no_faktur']
    if 'tanggal' in df.columns: faktur['TGL_FAKTUR'] = df['tanggal']
    if 'dpp' in df.columns: faktur['DPP'] = df['dpp']
    if 'ppn' in df.columns: faktur['PPN'] = df['ppn']
    if 'npwp' in df.columns: faktur['NPWP_LAWAN'] = df['npwp']
    f2 = f"{output_path}02_FakturMasuk_{timestamp}.csv"
    faktur.to_csv(f2, index=False); files_created.append(f2)

    # 03. BUPOT PPH
    bupot = pd.DataFrame()
    if 'no_bukti' in df.columns: bupot['NO_BUKTI_POTONG'] = df['no_bukti']
    if 'tanggal' in df.columns: bupot['TGL_BUKTI'] = df['tanggal']
    if 'npwp' in df.columns: bupot['NPWP_DIPOTONG'] = df['npwp']
    if 'jenis_pajak' in df.columns: bupot['JENIS_PAJAK'] = df['jenis_pajak']
    if 'dpp' in df.columns: bupot['DPP'] = df['dpp']
    if 'pph' in df.columns: bupot['PPh'] = df['pph']
    f3 = f"{output_path}03_Bupot_{timestamp}.csv"
    bupot.to_csv(f3, index=False); files_created.append(f3)

    # 04. PEMBAYARAN
    bayar = pd.DataFrame({'KETERANGAN':['Data Pembayaran']})
    f4 = f"{output_path}04_Pembayaran_{timestamp}.csv"
    bayar.to_csv(f4, index=False); files_created.append(f4)

    # 05. NTPN
    nt = pd.DataFrame({'KETERANGAN':['Data NTPN']})
    f5 = f"{output_path}05_NTPN_{timestamp}.csv"
    nt.to_csv(f5, index=False); files_created.append(f5)

    # 06. LAMPIRAN
    lamp = pd.DataFrame({'KETERANGAN':['Data Lampiran']})
    f6 = f"{output_path}06_Lampiran_{timestamp}.csv"
    lamp.to_csv(f6, index=False); files_created.append(f6)

    # 07. REKAP
    rekap = pd.DataFrame({'KETERANGAN':['Data Rekap']})
    f7 = f"{output_path}07_Rekap_{timestamp}.csv"
    rekap.to_csv(f7, index=False); files_created.append(f7)

    # 08. SPT INDUK
    spt = pd.DataFrame({'KETERANGAN':['Data SPT Induk']})
    f8 = f"{output_path}08_SPTInduk_{timestamp}.csv"
    spt.to_csv(f8, index=False); files_created.append(f8)

    return files_created