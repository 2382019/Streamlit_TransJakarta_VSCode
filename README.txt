# Dashboard Business Intelligence TransJakarta

## Persiapan
1. Instal Python 3.10 atau lebih baru.
2. Buka folder ini di Visual Studio Code.
3. Buka Terminal di VS Code.
4. Jalankan:
   ```bash
   python -m venv .venv
   ```
5. Aktifkan environment:
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - Windows CMD: `.venv\Scripts\activate.bat`
6. Instal library:
   ```bash
   pip install -r requirements.txt
   ```

## Menjalankan dashboard
Di terminal VS Code:
```bash
streamlit run app.py
```
Browser akan membuka dashboard Streamlit. Jika tidak terbuka otomatis, buka alamat lokal yang ditampilkan terminal (biasanya `http://localhost:8501`).

## Memakai dataset
Di panel kiri dashboard, unggah `dfTransjakarta180kRows.csv`.

Dashboard menyediakan KPI, tren harian, analisis koridor, durasi, kategori pembayaran, dan pemeriksaan kualitas data.

Catatan: dashboard menggunakan parser CSV yang mengikuti pendekatan perbaikan baris pada notebook yang diberikan. Cocokkan hasil dashboard dengan notebook dan instruksi dosen sebelum pengumpulan.
