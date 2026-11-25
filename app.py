import csv
import base64
from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ═══════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════
st.set_page_config(
    page_title="Dashboard TransJakarta",
    page_icon="🚌",
    layout="wide"
)

# ═══════════════════════════════════════════════
#  PALETA WARNA RESMI & FONT OPEN SANS
# ═══════════════════════════════════════════════
TJ_NAVY      = "#0D2B6E"  # Biru navy utama TransJakarta
TJ_BLUE      = "#1A56DB"  # Biru terang
TJ_SKY       = "#3B82F6"  # Biru langit
TJ_YELLOW    = "#FFB800"  # Kuning aksen bus TransJakarta
TJ_LIGHT_BG  = "#F8FAFC"  # Latar bersih
TJ_CARD_BG   = "#FFFFFF"  # Kartu putih
TJ_DARK_TEXT = "#002B5B"  # Teks gelap kontras tinggi
TJ_MUTED     = "#5A738E"  # Teks keterangan
TJ_BORDER    = "#D4E2F0"  # Garis border halus

css = f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    background-color: {TJ_LIGHT_BG} !important;
    color: {TJ_DARK_TEXT} !important;
}}

/* Judul & Headings */
h1, h2, h3, h4, [data-testid="stHeading"] {{
    font-family: 'Open Sans', sans-serif !important;
    color: {TJ_NAVY} !important;
    font-weight: 700 !important;
}}

/* Sidebar Resmi TransJakarta */
section[data-testid="stSidebar"] > div:first-child {{
    background: linear-gradient(180deg, {TJ_NAVY} 0%, #081C48 100%) !important;
    border-right: 3px solid {TJ_YELLOW};
}}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{
    color: {TJ_YELLOW} !important;
    font-weight: 700 !important;
}}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] label p,
section[data-testid="stSidebar"] label span {{
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}}

section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
    color: #CFE2FE !important;
}}

/* Input tanggal & teks di sidebar */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] [data-baseweb="input"],
section[data-testid="stSidebar"] [data-baseweb="input"] input,
section[data-testid="stSidebar"] [data-baseweb="input"] div,
section[data-testid="stSidebar"] [data-baseweb="input"] span {{
    color: {TJ_DARK_TEXT} !important;
    font-weight: 600 !important;
    background-color: #FFFFFF !important;
    border-radius: 8px !important;
}}

section[data-testid="stSidebar"] [data-baseweb="input"] svg {{
    fill: {TJ_NAVY} !important;
}}

/* File uploader di sidebar */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {{
    background: transparent !important;
}}

section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] {{
    background: #FFFFFF !important;
    border: 2px dashed {TJ_YELLOW} !important;
    border-radius: 10px !important;
}}

section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] * {{
    color: {TJ_DARK_TEXT} !important;
    font-weight: 500 !important;
}}

section[data-testid="stSidebar"] [data-testid="stFileUploaderFileData"] * {{
    color: {TJ_DARK_TEXT} !important;
    font-weight: 600 !important;
}}

/* Alert / Success box di sidebar */
section[data-testid="stSidebar"] [data-testid="stAlert"] {{
    background-color: #E6F4EA !important;
    border-left: 4px solid #137333 !important;
    border-radius: 8px !important;
}}

section[data-testid="stSidebar"] [data-testid="stAlert"] * {{
    color: #137333 !important;
    font-weight: 700 !important;
}}

/* KPI Metric Cards */
div[data-testid="metric-container"] {{
    background: {TJ_CARD_BG} !important;
    border: 1px solid {TJ_BORDER} !important;
    border-top: 3px solid {TJ_BLUE} !important;
    border-radius: 10px !important;
    padding: 18px 20px !important;
    box-shadow: 0 2px 10px rgba(13, 43, 110, 0.05) !important;
    transition: transform 0.2s, box-shadow 0.2s;
}}

div[data-testid="metric-container"]:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(13, 43, 110, 0.12) !important;
    border-top-color: {TJ_YELLOW} !important;
}}

div[data-testid="metric-container"] [data-testid="stMetricLabel"] {{
    color: {TJ_BLUE} !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color: {TJ_NAVY} !important;
    font-size: 1.65rem !important;
    font-weight: 800 !important;
}}

/* Tabs bergaya TransJakarta */
div[data-testid="stTabs"] [data-testid="stTab"] {{
    background: #EBF3FA !important;
    border: 1px solid {TJ_BORDER} !important;
    border-radius: 8px 8px 0 0;
    padding: 9px 20px !important;
    font-weight: 600 !important;
    color: {TJ_NAVY} !important;
}}

div[data-testid="stTabs"] [data-testid="stTab"]:hover {{
    background: #DCEAF7 !important;
}}

div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] {{
    background: {TJ_NAVY} !important;
    border-color: {TJ_NAVY} !important;
    color: #FFFFFF !important;
}}

div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] p {{
    color: #FFFFFF !important;
    font-weight: 700 !important;
}}

/* Desain Tabel / Dataframe */
div[data-testid="stDataFrame"] {{
    background-color: {TJ_CARD_BG} !important;
    border: 1px solid {TJ_BORDER} !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 8px rgba(13, 43, 110, 0.04) !important;
    overflow: hidden;
}}

/* Divider */
hr {{
    border: none !important;
    border-top: 1.5px solid {TJ_BORDER} !important;
    margin: 22px 0 !important;
}}
</style>"""
st.markdown(css, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  FUNGSI ENCODE GAMBAR BUS LISTRIK
# ═══════════════════════════════════════════════
def get_bus_b64():
    p = Path(__file__).parent / "bus_transjakarta.jpg"
    if p.exists():
        return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()
    return ""

bus_b64 = get_bus_b64()
if bus_b64:
    img_tag = f'<img src="{bus_b64}" style="width:100%;height:100%;object-fit:cover;border-radius:18px;" alt="Bus Listrik TransJakarta" />'
else:
    img_tag = '<div style="display:flex;align-items:center;justify-content:center;height:100%;font-size:3.5rem;">🚌</div>'

# ═══════════════════════════════════════════════
#  HEADER BANNER (KOTAK & GAMBAR SEJAJAR SEMPURNA)
# ═══════════════════════════════════════════════
header_html = f"""<div style="display:flex;gap:16px;align-items:stretch;margin-bottom:8px;">
<div style="flex:3.8;background:linear-gradient(135deg,#0D2B6E 0%,#1A56DB 60%,#1E40AF 100%);border-radius:18px;padding:22px 28px;box-shadow:0 8px 24px rgba(13,43,110,0.20);display:flex;flex-direction:column;justify-content:center;">
<div style="display:inline-block;width:fit-content;background:#FFB800;color:#0D2B6E;font-size:0.72rem;font-weight:800;padding:4px 12px;border-radius:20px;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:10px;">
🏙️ JAKARTA • BUSINESS INTELLIGENCE
</div>
<div style="font-size:1.85rem;font-weight:800;color:#FFFFFF;line-height:1.2;margin-bottom:8px;">
Dashboard <span style="color:#FFB800;">TransJakarta</span>
</div>
<div style="font-size:0.88rem;color:rgba(255,255,255,0.88);font-weight:500;">
🗓️ Periode: April 2023 &nbsp;|&nbsp; 🛣️ Analisis Transaksi BRT &nbsp;|&nbsp; ⚡ Bus Listrik &amp; Reguler
</div>
</div>
<div style="flex:1.2;border-radius:18px;overflow:hidden;box-shadow:0 8px 24px rgba(13,43,110,0.20);display:flex;align-items:center;justify-content:center;background:#FFFFFF;min-height:130px;">
{img_tag}
</div>
</div>
<div style="height:6px;background:repeating-linear-gradient(90deg,#0D2B6E 0px,#0D2B6E 22px,#FFB800 22px,#FFB800 44px,#1A56DB 44px,#1A56DB 66px,#3B82F6 66px,#3B82F6 88px);border-radius:4px;margin-bottom:24px;clear:both;"></div>"""
st.markdown(header_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════
st.sidebar.markdown(
    f"""<div style="text-align:center;padding:12px 0 6px;">
<div style="font-size:1.15rem;font-weight:800;color:{TJ_YELLOW};">🚌 TransJakarta BI</div>
<div style="font-size:0.75rem;color:rgba(255,255,255,0.65);margin-top:2px;">Business Intelligence Dashboard</div>
</div>""",
    unsafe_allow_html=True
)
st.sidebar.markdown("---")
st.sidebar.header("Pengaturan Data")
uploaded_file = st.sidebar.file_uploader(
    "Unggah dataset CSV",
    type=["csv"],
    help="Pilih file dataset CSV transaksi"
)

# ═══════════════════════════════════════════════
#  HELPER STYLE MATPLOTLIB
# ═══════════════════════════════════════════════
def apply_chart_style(fig, ax):
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FAFCFF")
    ax.tick_params(colors=TJ_DARK_TEXT, labelsize=9)
    ax.xaxis.label.set_color(TJ_DARK_TEXT)
    ax.yaxis.label.set_color(TJ_DARK_TEXT)
    ax.xaxis.label.set_fontweight("600")
    ax.yaxis.label.set_fontweight("600")
    for sp in ax.spines.values():
        sp.set_edgecolor(TJ_BORDER)
        sp.set_linewidth(1.0)
    ax.grid(True, color=TJ_BORDER, alpha=0.7, linestyle="--", linewidth=0.6)

# ═══════════════════════════════════════════════
#  LOAD DATA
# ═══════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_data(file_bytes):
    """Membaca CSV dengan penanganan baris yang dibungkus tanda kutip luar."""
    raw = file_bytes.decode("utf-8-sig")
    lines = raw.splitlines()

    if not lines:
        raise ValueError("File CSV kosong.")

    header = next(csv.reader([lines[0]]))
    rows = []
    failed_rows = []

    for line_number, line in enumerate(lines[1:], start=2):
        try:
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1].replace('""', '"')

            row = next(csv.reader([line]))
            if len(row) != len(header):
                failed_rows.append(line_number)
                continue
            rows.append(row)
        except Exception:
            failed_rows.append(line_number)

    data = pd.DataFrame(rows, columns=header)

    required = [
        "transID", "payCardBank", "corridorName", "tapInTime",
        "tapOutTime", "payAmount"
    ]
    missing_columns = [col for col in required if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing_columns}")

    data["transID"] = data["transID"].astype("string")
    data["payCardID"] = data["payCardID"].astype("string") if "payCardID" in data.columns else ""

    numeric_columns = [
        "payAmount", "tapInStopsLat", "tapInStopsLon",
        "tapOutStopsLat", "tapOutStopsLon", "direction",
        "stopStartSeq", "stopEndSeq", "payCardBirthDate"
    ]
    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    data["tapInTime"] = pd.to_datetime(data["tapInTime"], errors="coerce")
    data["tapOutTime"] = pd.to_datetime(data["tapOutTime"], errors="coerce")
    data["Durasi_Menit"] = (
        data["tapOutTime"] - data["tapInTime"]
    ).dt.total_seconds() / 60

    data["Tanggal"] = data["tapInTime"].dt.date
    data["corridorName"] = data["corridorName"].astype("string").str.strip()
    data["payCardBank"] = data["payCardBank"].astype("string").str.strip()

    return data, failed_rows

# ═══════════════════════════════════════════════
#  HALAMAN AWAL SEBELUM UPLOAD (KARTU ESTETIK)
# ═══════════════════════════════════════════════
if uploaded_file is None:
    welcome_card = f"""<div style="background:#FFFFFF;border:1px solid {TJ_BORDER};border-left:5px solid {TJ_NAVY};border-radius:12px;padding:24px 28px;box-shadow:0 4px 16px rgba(13,43,110,0.06);margin-top:6px;">
<div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
<span style="font-size:1.6rem;">🚏</span>
<span style="font-size:1.15rem;font-weight:700;color:{TJ_NAVY};">Menunggu Unggahan Dataset TransJakarta</span>
</div>
<p style="color:{TJ_MUTED};font-size:0.92rem;line-height:1.6;margin:0 0 16px 0;">
Silakan pilih atau seret file CSV transaksi Anda melalui panel di sebelah kiri untuk memulai eksplorasi analitik dashboard secara interaktif.
</p>
<div style="background:{TJ_LIGHT_BG};border:1px dashed {TJ_BORDER};border-radius:10px;padding:16px 20px;">
<div style="font-weight:700;color:{TJ_NAVY};font-size:0.9rem;margin-bottom:8px;display:flex;align-items:center;gap:8px;">
<span>📊</span> Analitik yang Akan Ditampilkan:
</div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;">
<div style="display:flex;align-items:center;gap:8px;color:{TJ_DARK_TEXT};font-size:0.86rem;">
<span style="color:{TJ_BLUE};font-weight:bold;">✔</span> Ringkasan Indikator Utama (KPI)
</div>
<div style="display:flex;align-items:center;gap:8px;color:{TJ_DARK_TEXT};font-size:0.86rem;">
<span style="color:{TJ_BLUE};font-weight:bold;">✔</span> Tren Fluktuasi Transaksi Harian
</div>
<div style="display:flex;align-items:center;gap:8px;color:{TJ_DARK_TEXT};font-size:0.86rem;">
<span style="color:{TJ_BLUE};font-weight:bold;">✔</span> 10 Koridor Terpadat Penumpang
</div>
<div style="display:flex;align-items:center;gap:8px;color:{TJ_DARK_TEXT};font-size:0.86rem;">
<span style="color:{TJ_BLUE};font-weight:bold;">✔</span> 10 Koridor dengan Rata-rata Durasi Terlama
</div>
<div style="display:flex;align-items:center;gap:8px;color:{TJ_DARK_TEXT};font-size:0.86rem;">
<span style="color:{TJ_BLUE};font-weight:bold;">✔</span> Distribusi Kartu &amp; Bank Pembayaran
</div>
<div style="display:flex;align-items:center;gap:8px;color:{TJ_DARK_TEXT};font-size:0.86rem;">
<span style="color:{TJ_BLUE};font-weight:bold;">✔</span> Pemeriksaan Integritas &amp; Kualitas Data
</div>
</div>
</div>
</div>"""
    st.markdown(welcome_card, unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════
#  PROSES PEMBACAAN DATA
# ═══════════════════════════════════════════════
try:
    with st.spinner("🚌 Membaca dan membersihkan dataset TransJakarta..."):
        df, failed_rows = load_data(uploaded_file.getvalue())
except Exception as error:
    st.error(f"Gagal membaca dataset: {error}")
    st.stop()

st.sidebar.success(f"{len(df):,} baris berhasil dibaca")
if failed_rows:
    st.sidebar.warning(f"{len(failed_rows):,} baris dilewati karena format tidak sesuai.")
else:
    st.sidebar.caption("Semua baris data berhasil dibaca dengan parser.")

# Filter tanggal
valid_dates = df["Tanggal"].dropna()
if not valid_dates.empty:
    min_date = min(valid_dates)
    max_date = max(valid_dates)
    date_range = st.sidebar.date_input(
        "Filter rentang tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        view = df[
            df["Tanggal"].notna()
            & (df["Tanggal"] >= start_date)
            & (df["Tanggal"] <= end_date)
        ].copy()
    else:
        view = df.copy()
else:
    view = df.copy()

if view.empty:
    st.warning("Tidak ada transaksi pada rentang tanggal yang dipilih.")
    st.stop()

# ═══════════════════════════════════════════════
#  RINGKASAN KPI
# ═══════════════════════════════════════════════
total_transactions = len(view)
valid_corridors = view[
    view["corridorName"].notna() & view["corridorName"].ne("")
]
corridor_count = valid_corridors["corridorName"].nunique()
mean_duration = view.loc[
    view["Durasi_Menit"].notna() & (view["Durasi_Menit"] >= 0),
    "Durasi_Menit"
].mean()
payment_total = view["payAmount"].sum(min_count=1)
missing_payment = view["payAmount"].isna().sum()
missing_tapout = view["tapOutTime"].isna().sum()

st.subheader("Ringkasan KPI")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Transaksi", f"{total_transactions:,.0f}")
k2.metric("Koridor Unik", f"{corridor_count:,.0f}")
k3.metric("Rata-rata Durasi", f"{mean_duration:.2f} menit" if pd.notna(mean_duration) else "Tidak tersedia")
k4.metric("Pembayaran Tercatat", f"Rp {payment_total:,.0f}" if pd.notna(payment_total) else "Tidak tersedia")

k5, k6 = st.columns(2)
k5.metric("Pembayaran Kosong", f"{missing_payment:,.0f}")
k6.metric("Waktu Tap-out Kosong", f"{missing_tapout:,.0f}")

st.divider()

# ═══════════════════════════════════════════════
#  TABS ANALISIS (DENGAN TABEL ESTETIK BEBAS UNDERSCORE)
# ═══════════════════════════════════════════════
tab_overview, tab_corridor, tab_duration, tab_payment, tab_quality = st.tabs([
    "📈 Ikhtisar", "🛣️ Koridor", "⏱️ Durasi", "💳 Pembayaran", "🔍 Kualitas Data"
])

# ── TAB 1: IKHTISAR ──────────────────────────
with tab_overview:
    st.subheader("Tren Transaksi Harian")
    daily = view.dropna(subset=["Tanggal"]).groupby("Tanggal")["transID"].count().sort_index()
    if not daily.empty:
        # Elemen lencana ringkasan analitik
        st.markdown(
            f"""<div style="display:flex;gap:12px;margin-bottom:14px;flex-wrap:wrap;">
<span style="background:#EBF3FA;border:1px solid #D4E2F0;padding:6px 14px;border-radius:20px;font-size:0.85rem;color:{TJ_NAVY};font-weight:600;">
📅 Rentang: <strong>{min(daily.index)}</strong> s.d. <strong>{max(daily.index)}</strong>
</span>
<span style="background:#EBF3FA;border:1px solid #D4E2F0;padding:6px 14px;border-radius:20px;font-size:0.85rem;color:{TJ_NAVY};font-weight:600;">
📈 Rata-rata Harian: <strong>{daily.mean():,.0f} transaksi</strong>
</span>
<span style="background:#EBF3FA;border:1px solid #D4E2F0;padding:6px 14px;border-radius:20px;font-size:0.85rem;color:{TJ_NAVY};font-weight:600;">
🚀 Puncak Tertinggi: <strong>{daily.max():,.0f} transaksi</strong> ({daily.idxmax()})
</span>
</div>""",
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(figsize=(12, 4))
        apply_chart_style(fig, ax)

        x = list(range(len(daily)))
        ax.fill_between(x, daily.values, alpha=0.18, color=TJ_BLUE)
        ax.plot(
            x, daily.values, marker="o", linewidth=2.2, color=TJ_NAVY,
            markerfacecolor=TJ_BLUE, markeredgecolor="#FFFFFF", markeredgewidth=1.5,
            markersize=6, zorder=5
        )

        ax.set_xticks(x)
        ax.set_xticklabels([str(d) for d in daily.index], rotation=45, ha="right", fontsize=8.5, color=TJ_DARK_TEXT)
        ax.set_xlabel("Tanggal Perjalanan")
        ax.set_ylabel("Jumlah Transaksi")
        ax.set_title("Distribusi Transaksi per Hari", color=TJ_NAVY, fontsize=12, fontweight="bold", pad=10)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Tidak ada tanggal valid untuk ditampilkan.")

    st.caption("Catatan: Perhatikan tanggal dengan jumlah transaksi jauh lebih rendah yang dipengaruhi oleh akhir pekan atau hari libur nasional.")

# ── TAB 2: KORIDOR ───────────────────────────
with tab_corridor:
    st.subheader("10 Koridor dengan Transaksi Terbanyak")
    corridor_counts = (
        valid_corridors.groupby("corridorName")["transID"]
        .count().sort_values(ascending=False).head(10)
    )
    if not corridor_counts.empty:
        sorted_cc = corridor_counts.sort_values()
        n = len(sorted_cc)
        top1_kor = sorted_cc.index[-1]
        top1_val = sorted_cc.values[-1]

        # Elemen lencana estetik
        st.markdown(
            f"""<div style="display:flex;gap:12px;margin-bottom:14px;flex-wrap:wrap;">
<span style="background:#EBF3FA;border:1px solid #D4E2F0;padding:6px 14px;border-radius:20px;font-size:0.85rem;color:{TJ_NAVY};font-weight:600;">
🥇 Koridor Terpadat: <strong>{top1_kor}</strong> ({top1_val:,} transaksi)
</span>
<span style="background:#EBF3FA;border:1px solid #D4E2F0;padding:6px 14px;border-radius:20px;font-size:0.85rem;color:{TJ_NAVY};font-weight:600;">
🛣️ Total Koridor Aktif: <strong>{corridor_count} koridor</strong>
</span>
</div>""",
            unsafe_allow_html=True
        )

        bar_colors = plt.cm.Blues(np.linspace(0.45, 0.95, n))

        fig, ax = plt.subplots(figsize=(11, 4.8))
        apply_chart_style(fig, ax)
        bars = ax.barh(range(n), sorted_cc.values, color=bar_colors, edgecolor="#FFFFFF", linewidth=1, height=0.62)
        for i, val in enumerate(sorted_cc.values):
            ax.text(val + sorted_cc.values.max() * 0.01, i, f"{val:,}",
                    va="center", ha="left", color=TJ_NAVY, fontsize=8.5, fontweight="700")

        ax.set_yticks(range(n))
        ax.set_yticklabels(sorted_cc.index, fontsize=8.5, color=TJ_DARK_TEXT)
        ax.set_xlabel("Jumlah Transaksi")
        ax.set_ylabel("Nama Koridor")
        ax.set_title("Top 10 Koridor — Volume Penumpang", color=TJ_NAVY, fontsize=12, fontweight="bold", pad=10)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        # Tabel estetik tanpa underscore dengan kolom persentase
        corridor_summary = corridor_counts.reset_index()
        corridor_summary.columns = ["Nama Koridor", "Jumlah Transaksi"]
        total_valid = valid_corridors["transID"].count()
        corridor_summary["Pangsa Transaksi"] = (corridor_summary["Jumlah Transaksi"] / total_valid) * 100
        corridor_summary.insert(0, "No", range(1, len(corridor_summary) + 1))

        st.dataframe(
            corridor_summary,
            column_config={
                "No": st.column_config.NumberColumn("No", format="%d", alignment="center", width="small"),
                "Nama Koridor": st.column_config.TextColumn("🚏 Nama Koridor", help="Rute jalur BRT TransJakarta"),
                "Jumlah Transaksi": st.column_config.NumberColumn("🎫 Jumlah Transaksi", format="%d", alignment="center"),
                "Pangsa Transaksi": st.column_config.NumberColumn("📊 Pangsa Pasar", format="%.2f%%", alignment="center"),
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Tidak ada nama koridor valid pada filter ini.")

# ── TAB 3: DURASI ────────────────────────────
with tab_duration:
    st.subheader("10 Koridor dengan Rata-rata Durasi Terlama")
    duration_data = view[
        view["corridorName"].notna()
        & view["corridorName"].ne("")
        & view["Durasi_Menit"].notna()
        & (view["Durasi_Menit"] >= 0)
    ]
    duration_by_corridor = (
        duration_data.groupby("corridorName")
        .agg(
            Jumlah_Transaksi=("transID", "count"),
            Rata_rata_Durasi=("Durasi_Menit", "mean"),
            Median_Durasi=("Durasi_Menit", "median")
        )
        .sort_values("Rata_rata_Durasi", ascending=False)
    )
    top_duration = duration_by_corridor.head(10)
    if not top_duration.empty:
        sorted_td = top_duration["Rata_rata_Durasi"].sort_values()
        n = len(sorted_td)
        longest_kor = sorted_td.index[-1]
        longest_val = sorted_td.values[-1]

        # Elemen lencana estetik
        st.markdown(
            f"""<div style="display:flex;gap:12px;margin-bottom:14px;flex-wrap:wrap;">
<span style="background:#EBF3FA;border:1px solid #D4E2F0;padding:6px 14px;border-radius:20px;font-size:0.85rem;color:{TJ_NAVY};font-weight:600;">
⏱️ Durasi Terlama: <strong>{longest_kor}</strong> ({longest_val:.1f} menit)
</span>
<span style="background:#EBF3FA;border:1px solid #D4E2F0;padding:6px 14px;border-radius:20px;font-size:0.85rem;color:{TJ_NAVY};font-weight:600;">
⏳ Rata-rata Seluruh Perjalanan: <strong>{mean_duration:.1f} menit</strong>
</span>
</div>""",
            unsafe_allow_html=True
        )

        bar_colors = plt.cm.Blues(np.linspace(0.45, 0.95, n))

        fig, ax = plt.subplots(figsize=(11, 4.8))
        apply_chart_style(fig, ax)
        bars = ax.barh(range(n), sorted_td.values, color=bar_colors, edgecolor="#FFFFFF", linewidth=1, height=0.62)
        for i, val in enumerate(sorted_td.values):
            ax.text(val + sorted_td.values.max() * 0.01, i, f"{val:.1f} mnt",
                    va="center", ha="left", color=TJ_NAVY, fontsize=8.5, fontweight="700")

        ax.set_yticks(range(n))
        ax.set_yticklabels(sorted_td.index, fontsize=8.5, color=TJ_DARK_TEXT)
        ax.set_xlabel("Rata-rata Durasi (menit)")
        ax.set_ylabel("Nama Koridor")
        ax.set_title("Top 10 Koridor — Durasi Perjalanan Rata-rata", color=TJ_NAVY, fontsize=12, fontweight="bold", pad=10)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        # Tabel estetik tanpa underscore
        top_dur_df = top_duration.reset_index()
        top_dur_df.columns = ["Nama Koridor", "Jumlah Transaksi", "Rata-rata Durasi (Menit)", "Median Durasi (Menit)"]
        top_dur_df.insert(0, "No", range(1, len(top_dur_df) + 1))

        st.dataframe(
            top_dur_df,
            column_config={
                "No": st.column_config.NumberColumn("No", format="%d", alignment="center", width="small"),
                "Nama Koridor": st.column_config.TextColumn("🚏 Nama Koridor"),
                "Jumlah Transaksi": st.column_config.NumberColumn("🎫 Volume Transaksi", format="%d", alignment="center"),
                "Rata-rata Durasi (Menit)": st.column_config.NumberColumn("⏱️ Rata-rata Durasi", format="%.2f menit", alignment="center"),
                "Median Durasi (Menit)": st.column_config.NumberColumn("⌛ Median Durasi", format="%.2f menit", alignment="center"),
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Belum ada durasi valid untuk dihitung.")
    st.caption("Catatan: Durasi lebih lama dipengaruhi oleh panjang lintasan rute serta frekuensi titik pemberhentian halte.")

# ── TAB 4: PEMBAYARAN ────────────────────────
with tab_payment:
    st.subheader("Transaksi Berdasarkan Kategori Pembayaran")
    bank_data = view[
        view["payCardBank"].notna() & view["payCardBank"].ne("")
    ]
    bank_summary = (
        bank_data.groupby("payCardBank")
        .agg(
            Jumlah_Transaksi=("transID", "count"),
            Total_Pembayaran=("payAmount", "sum"),
            Pembayaran_Kosong=("payAmount", lambda x: x.isna().sum())
        )
        .sort_values("Jumlah_Transaksi", ascending=False)
    )
    if not bank_summary.empty:
        top_bank_name = bank_summary.index[0]
        top_bank_tx = bank_summary["Jumlah_Transaksi"].iloc[0]

        # Elemen lencana estetik
        st.markdown(
            f"""<div style="display:flex;gap:12px;margin-bottom:14px;flex-wrap:wrap;">
<span style="background:#EBF3FA;border:1px solid #D4E2F0;padding:6px 14px;border-radius:20px;font-size:0.85rem;color:{TJ_NAVY};font-weight:600;">
🏆 Metode Terpopuler: <strong>{top_bank_name}</strong> ({top_bank_tx:,} transaksi)
</span>
<span style="background:#EBF3FA;border:1px solid #D4E2F0;padding:6px 14px;border-radius:20px;font-size:0.85rem;color:{TJ_NAVY};font-weight:600;">
💳 Total Mitra Pembayaran: <strong>{len(bank_summary)} bank/kartu</strong>
</span>
</div>""",
            unsafe_allow_html=True
        )

        col_bar, col_pie = st.columns([3, 2])

        with col_bar:
            sorted_bs = bank_summary["Jumlah_Transaksi"].sort_values()
            n = len(sorted_bs)
            bar_colors = [TJ_NAVY if i % 2 == 0 else TJ_BLUE for i in range(n)]

            fig, ax = plt.subplots(figsize=(8, max(3, n * 0.75)))
            apply_chart_style(fig, ax)
            bars = ax.barh(range(n), sorted_bs.values, color=bar_colors, edgecolor="#FFFFFF", linewidth=1, height=0.6)
            for i, val in enumerate(sorted_bs.values):
                ax.text(val * 0.97, i, f"{val:,}", va="center", ha="right",
                        color="#FFFFFF", fontsize=8.5, fontweight="700")

            ax.set_yticks(range(n))
            ax.set_yticklabels(sorted_bs.index, fontsize=9, color=TJ_DARK_TEXT)
            ax.set_xlabel("Jumlah Transaksi")
            ax.set_ylabel("Kategori Pembayaran")
            ax.set_title("Volume per Bank", color=TJ_NAVY, fontsize=11, fontweight="bold", pad=10)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with col_pie:
            top5 = bank_summary["Jumlah_Transaksi"].head(5)
            pie_colors = [TJ_NAVY, TJ_BLUE, TJ_SKY, "#33A8E8", "#A8D4F2"]

            fig2, ax2 = plt.subplots(figsize=(5, 5))
            fig2.patch.set_facecolor("#FFFFFF")
            ax2.set_facecolor("#FFFFFF")
            wedges, texts, autotexts = ax2.pie(
                top5.values,
                labels=top5.index,
                colors=pie_colors,
                autopct="%1.1f%%",
                startangle=140,
                wedgeprops={"edgecolor": "#FFFFFF", "linewidth": 2},
                textprops={"color": TJ_DARK_TEXT, "fontsize": 8.5, "fontweight": "600"}
            )
            for at in autotexts:
                at.set_color("#FFFFFF")
                at.set_fontweight("bold")
            ax2.set_title("Pangsa Pasar Top 5 Bank", color=TJ_NAVY, fontsize=11, fontweight="bold")
            fig2.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)

        # Tabel estetik tanpa underscore dengan format Rupiah
        bank_df = bank_summary.reset_index()
        bank_df.columns = ["Penerbit Kartu / Bank", "Jumlah Transaksi", "Total Pembayaran (Rp)", "Pembayaran Tanpa Nilai"]
        bank_df["Pangsa Transaksi"] = (bank_df["Jumlah Transaksi"] / total_transactions) * 100
        bank_df.insert(0, "No", range(1, len(bank_df) + 1))

        st.dataframe(
            bank_df,
            column_config={
                "No": st.column_config.NumberColumn("No", format="%d", alignment="center", width="small"),
                "Penerbit Kartu / Bank": st.column_config.TextColumn("💳 Bank / Kartu Pembayaran"),
                "Jumlah Transaksi": st.column_config.NumberColumn("🎫 Jumlah Transaksi", format="%d", alignment="center"),
                "Total Pembayaran (Rp)": st.column_config.NumberColumn("💰 Total Pembayaran", format="Rp %d", alignment="center"),
                "Pembayaran Tanpa Nilai": st.column_config.NumberColumn("❓ Nilai Kosong", format="%d", alignment="center"),
                "Pangsa Transaksi": st.column_config.NumberColumn(
                    "📊 Pangsa Penggunaan",
                    format="%.2f%%",
                    alignment="center"
                )
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Tidak ada kategori pembayaran valid.")

# ── TAB 5: KUALITAS DATA ─────────────────────
with tab_quality:
    st.subheader("Pemeriksaan Kualitas Data")

    # Elemen lencana estetik
    st.markdown(
        f"""<div style="display:flex;gap:12px;margin-bottom:14px;flex-wrap:wrap;">
<span style="background:#EBF3FA;border:1px solid #D4E2F0;padding:6px 14px;border-radius:20px;font-size:0.85rem;color:{TJ_NAVY};font-weight:600;">
🛡️ Total Sampel Terverifikasi: <strong>{total_transactions:,} baris</strong>
</span>
<span style="background:#E6F4EA;border:1px solid #A8DAB5;padding:6px 14px;border-radius:20px;font-size:0.85rem;color:#137333;font-weight:600;">
✅ Parameter Integritas Data Siap Dianalisis
</span>
</div>""",
        unsafe_allow_html=True
    )

    quality = pd.DataFrame({
        "Parameter Pemeriksaan": [
            "Total baris data tersaring",
            "ID transaksi terduplikasi",
            "Nilai pembayaran kosong",
            "Waktu tap-in kosong",
            "Waktu tap-out kosong",
            "Durasi perjalanan negatif",
            "Baris gagal dibaca pada berkas"
        ],
        "Jumlah Baris": [
            len(view),
            view["transID"].duplicated().sum(),
            view["payAmount"].isna().sum(),
            view["tapInTime"].isna().sum(),
            view["tapOutTime"].isna().sum(),
            (view["Durasi_Menit"] < 0).sum(),
            len(failed_rows)
        ]
    })

    def badge(v, lbl):
        if lbl == "Total baris data tersaring":
            return "✅ Terpenuhi"
        if v == 0:
            return "✅ Bersih"
        if v < 100:
            return "⚠️ Perlu Ditinjau"
        return "🔴 Perlu Tindakan"

    quality["Status Data"] = [badge(r["Jumlah Baris"], r["Parameter Pemeriksaan"]) for _, r in quality.iterrows()]
    quality.insert(0, "No", range(1, len(quality) + 1))

    # Tabel estetik tanpa underscore
    st.dataframe(
        quality,
        column_config={
            "No": st.column_config.NumberColumn("No", format="%d", alignment="center", width="small"),
            "Parameter Pemeriksaan": st.column_config.TextColumn("📋 Parameter Integritas Data"),
            "Jumlah Baris": st.column_config.NumberColumn("📊 Jumlah Baris", format="%d", alignment="center"),
            "Status Data": st.column_config.TextColumn("📌 Status", alignment="center"),
        },
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        "Catatan Keterbatasan Data: Nilai kosong dipertahankan untuk mencerminkan kondisi riil sistem tap-in & tap-out di lapangan."
    )
