import csv
import base64
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import streamlit as st

# ═══════════════════════════════════════════════
#  WARNA TEMA
# ═══════════════════════════════════════════════
NAVY       = "#0D2B6E"
BLUE       = "#1A56DB"
SKY        = "#3B82F6"
LIGHT_BLUE = "#DBEAFE"
YELLOW     = "#FFB800"
GOLD       = "#F59E0B"
WHITE      = "#FFFFFF"
OFF_WHITE  = "#F4F7FF"
GRAY_DARK  = "#1E293B"
GRAY_MID   = "#64748B"
GRAY_LIGHT = "#E2E8F0"
SUCCESS    = "#059669"
DANGER     = "#DC2626"
WARN_CLR   = "#D97706"

# ═══════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════
st.set_page_config(page_title="Dashboard TransJakarta", page_icon="🚌", layout="wide")

# ═══════════════════════════════════════════════
#  CSS (singkat, targeted)
# ═══════════════════════════════════════════════
css = """
<style>
.stApp {background-color: #F4F7FF !important;}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #0D2B6E 0%, #0F1E4A 100%) !important;
    border-right: 3px solid #FFB800;
}

/* Judul & label langsung di sidebar (di atas background navy) */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {color: #FFB800 !important;}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] label p,
section[data-testid="stSidebar"] label span {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}

section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #E2E8F0 !important;
}

/* ── KOTAK INPUT (Date Picker, Text Input, dll.) -> FONT GELAP TEGAS ── */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] [data-baseweb="input"],
section[data-testid="stSidebar"] [data-baseweb="input"] input,
section[data-testid="stSidebar"] [data-baseweb="input"] div,
section[data-testid="stSidebar"] [data-baseweb="input"] span {
    color: #0F172A !important;
    font-weight: 600 !important;
    background-color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [data-baseweb="input"] svg {
    fill: #0F172A !important;
}

/* ── FILE UPLOADER (Kotak upload & info file) -> FONT GELAP TEGAS ── */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: transparent !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] {
    background: #FFFFFF !important;
    border: 2px dashed #FFB800 !important;
    border-radius: 12px !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] *,
section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] p,
section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] span,
section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] small {
    color: #1E293B !important;
    font-weight: 500 !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderFileData"],
section[data-testid="stSidebar"] [data-testid="stFileUploaderFileData"] * {
    color: #0F172A !important;
    font-weight: 600 !important;
}

/* ── ALERT BOXES (Success, Warning, Error di Sidebar) -> FONT GELAP TEGAS ── */
section[data-testid="stSidebar"] [data-testid="stAlert"] {
    border-radius: 10px !important;
}

section[data-testid="stSidebar"] [data-testid="stAlert"] p,
section[data-testid="stSidebar"] [data-testid="stAlert"] span,
section[data-testid="stSidebar"] [data-testid="stAlert"] div {
    color: #064E3B !important;
    font-weight: 700 !important;
}

/* Jika ada warning di sidebar */
section[data-testid="stSidebar"] [data-testid="stAlert"][data-baseweb*="warning"] * {
    color: #78350F !important;
    font-weight: 700 !important;
}

/* ── Headings di Konten Utama ── */
.stApp h1, .stApp h2, .stApp h3 {color: #0D2B6E !important; font-weight: 700 !important;}

/* ── KPI Cards ── */
div[data-testid="metric-container"] {
    background: #FFFFFF !important;
    border: 1px solid #DBEAFE !important;
    border-top: 4px solid #1A56DB !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
    box-shadow: 0 4px 16px rgba(13,43,110,0.10) !important;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(13,43,110,0.18) !important;
    border-top-color: #FFB800 !important;
}
div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #64748B !important; font-weight: 600 !important;
    text-transform: uppercase; letter-spacing: 0.06em;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #0D2B6E !important; font-weight: 800 !important;
}

/* ── Tabs ── */
div[data-testid="stTabs"] [data-testid="stTab"] {
    background: #FFFFFF !important; border: 1px solid #DBEAFE !important;
    border-radius: 10px 10px 0 0;
}
div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] {
    background: linear-gradient(180deg, #FFB800, #E6A500) !important;
    border-color: #FFB800 !important;
}
div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] p {
    color: #0D2B6E !important; font-weight: 700;
}

/* ── Dataframe ── */
div[data-testid="stDataFrame"] {
    border: 1px solid #DBEAFE !important; border-radius: 12px !important;
}

/* ── Divider ── */
hr {border: none !important; border-top: 2px solid #DBEAFE !important; margin: 24px 0 !important;}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  HEADER — Streamlit native (pasti tampil)
# ═══════════════════════════════════════════════
header_html = (
    '<div style="background:linear-gradient(135deg,#0D2B6E 0%,#1A56DB 60%,#1E40AF 100%);'
    'border-radius:18px;padding:28px 36px;margin-bottom:6px;'
    'box-shadow:0 10px 40px rgba(13,43,110,0.30);">'
    '<div style="display:inline-block;background:#FFB800;color:#0D2B6E;'
    'font-size:0.72rem;font-weight:700;padding:4px 14px;border-radius:20px;'
    'margin-bottom:12px;letter-spacing:0.08em;text-transform:uppercase;">'
    '🏙️ Jakarta • Business Intelligence</div>'
    '<div style="font-size:1.9rem;font-weight:800;color:#FFFFFF;'
    'line-height:1.2;margin-bottom:10px;">'
    'Dashboard <span style="color:#FFB800;">TransJakarta</span></div>'
    '<div style="font-size:0.88rem;color:rgba(255,255,255,0.85);">'
    '📅 Periode: April 2023 &nbsp;|&nbsp; '
    '🛣️ Analisis Transaksi BRT &nbsp;|&nbsp; '
    '⚡ Bus Listrik &amp; Reguler</div>'
    '</div>'
)

stripe_html = (
    '<div style="height:5px;background:repeating-linear-gradient(90deg,'
    '#0D2B6E 0px,#0D2B6E 22px,#FFB800 22px,#FFB800 44px,'
    '#1A56DB 44px,#1A56DB 66px,#3B82F6 66px,#3B82F6 88px);'
    'border-radius:0 0 6px 6px;margin-bottom:8px;"></div>'
)

col_hdr, col_img = st.columns([4, 1])
with col_hdr:
    st.markdown(header_html, unsafe_allow_html=True)
with col_img:
    bus_path = Path(__file__).parent / "bus_transjakarta.jpg"
    if bus_path.exists():
        st.image(str(bus_path), use_container_width=True)
    else:
        st.markdown("### 🚌")

st.markdown(stripe_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════
sb_brand = (
    '<div style="text-align:center;padding:18px 0 6px;">'
    '<div style="font-size:1.1rem;font-weight:800;color:#FFB800;">🚌 TransJakarta BI</div>'
    '<div style="font-size:0.75rem;color:rgba(255,255,255,0.55);margin-top:4px;">'
    'Business Intelligence Dashboard</div></div>'
)
st.sidebar.markdown(sb_brand, unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Pengaturan Data")

uploaded_file = st.sidebar.file_uploader(
    "Unggah dataset CSV", type=["csv"],
    help="Pilih file dfTransjakarta180kRows.csv"
)

# ═══════════════════════════════════════════════
#  MATPLOTLIB HELPERS
# ═══════════════════════════════════════════════
def apply_style(fig, ax):
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor("#F8FAFF")
    ax.tick_params(colors=GRAY_MID, labelsize=9)
    ax.xaxis.label.set_color(GRAY_MID)
    ax.yaxis.label.set_color(GRAY_MID)
    for sp in ax.spines.values():
        sp.set_edgecolor(GRAY_LIGHT)
    ax.grid(True, color=GRAY_LIGHT, alpha=0.9, linestyle="--", linewidth=0.6)

def safe_cmap(name):
    try:
        return matplotlib.colormaps[name]
    except (AttributeError, KeyError):
        return plt.cm.get_cmap(name)

# ═══════════════════════════════════════════════
#  LOAD DATA
# ═══════════════════════════════════════════════
@st.cache_data(show_spinner="🚌 Membaca dan membersihkan dataset...")
def load_data(file_bytes):
    raw = file_bytes.decode("utf-8-sig")
    lines = raw.splitlines()
    if not lines:
        raise ValueError("File CSV kosong.")

    header = next(csv.reader([lines[0]]))
    rows, failed = [], []

    for ln, line in enumerate(lines[1:], start=2):
        try:
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1].replace('""', '"')
            row = next(csv.reader([line]))
            if len(row) != len(header):
                failed.append(ln)
                continue
            rows.append(row)
        except Exception:
            failed.append(ln)

    data = pd.DataFrame(rows, columns=header)

    need = ["transID","payCardBank","corridorName","tapInTime","tapOutTime","payAmount"]
    miss = [c for c in need if c not in data.columns]
    if miss:
        raise ValueError(f"Kolom wajib tidak ditemukan: {miss}")

    data["transID"] = data["transID"].astype("string")
    if "payCardID" in data.columns:
        data["payCardID"] = data["payCardID"].astype("string")

    for c in ["payAmount","tapInStopsLat","tapInStopsLon","tapOutStopsLat",
              "tapOutStopsLon","direction","stopStartSeq","stopEndSeq","payCardBirthDate"]:
        if c in data.columns:
            data[c] = pd.to_numeric(data[c], errors="coerce")

    data["tapInTime"]    = pd.to_datetime(data["tapInTime"],  errors="coerce")
    data["tapOutTime"]   = pd.to_datetime(data["tapOutTime"], errors="coerce")
    data["Durasi_Menit"] = (data["tapOutTime"] - data["tapInTime"]).dt.total_seconds() / 60
    data["Tanggal"]      = data["tapInTime"].dt.date
    data["corridorName"] = data["corridorName"].astype("string").str.strip()
    data["payCardBank"]  = data["payCardBank"].astype("string").str.strip()
    return data, failed

# ═══════════════════════════════════════════════
#  HALAMAN AWAL (sebelum upload)
# ═══════════════════════════════════════════════
if uploaded_file is None:
    st.info("🚏 Silakan unggah file CSV melalui panel sebelah kiri untuk memulai dashboard.")

    st.markdown("#### 📂 File yang digunakan")
    st.code("dfTransjakarta180kRows.csv", language=None)

    st.markdown("#### Dashboard akan menampilkan:")
    st.markdown("""
| | Fitur |
|---|---|
| 🔢 | KPI utama transaksi |
| 📈 | Tren transaksi harian |
| 🛣️ | 10 koridor dengan transaksi terbanyak |
| ⏱️ | 10 koridor dengan rata-rata durasi terlama |
| 💳 | Transaksi berdasarkan kategori pembayaran |
| 🔍 | Pemeriksaan kualitas data |
""")
    st.stop()

try:
    df, failed_rows = load_data(uploaded_file.getvalue())
except Exception as error:
    st.error(f"❌ Gagal membaca dataset: {error}")
    st.stop()

st.sidebar.success(f"✅ {len(df):,} baris berhasil dibaca")
if failed_rows:
    st.sidebar.warning(f"⚠️ {len(failed_rows):,} baris dilewati (format tidak sesuai).")
else:
    st.sidebar.caption("✔️ Semua baris berhasil dibaca.")

# Filter tanggal
valid_dates = df["Tanggal"].dropna()
if not valid_dates.empty:
    min_d, max_d = min(valid_dates), max(valid_dates)
    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Filter Tanggal")
    date_range = st.sidebar.date_input(
        "Rentang tanggal", value=(min_d, max_d),
        min_value=min_d, max_value=max_d
    )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        s, e = date_range
        view = df[df["Tanggal"].notna() & (df["Tanggal"] >= s) & (df["Tanggal"] <= e)].copy()
    else:
        view = df.copy()
else:
    view = df.copy()

if view.empty:
    st.warning("⚠️ Tidak ada transaksi pada rentang tanggal yang dipilih.")
    st.stop()

# ═══════════════════════════════════════════════
#  KPI
# ═══════════════════════════════════════════════
total_tx     = len(view)
valid_cor    = view[view["corridorName"].notna() & view["corridorName"].ne("")]
corridor_cnt = valid_cor["corridorName"].nunique()
mean_dur     = view.loc[view["Durasi_Menit"].notna() & (view["Durasi_Menit"] >= 0), "Durasi_Menit"].mean()
pay_total    = view["payAmount"].sum(min_count=1)
miss_pay     = view["payAmount"].isna().sum()
miss_tap     = view["tapOutTime"].isna().sum()

st.subheader("📊 Ringkasan KPI")
k1, k2, k3, k4 = st.columns(4)
k1.metric("🎫 Total Transaksi",     f"{total_tx:,.0f}")
k2.metric("🛣️ Koridor Unik",        f"{corridor_cnt:,.0f}")
k3.metric("⏱️ Rata-rata Durasi",    f"{mean_dur:.2f} menit" if pd.notna(mean_dur) else "N/A")
k4.metric("💰 Pembayaran Tercatat", f"Rp {pay_total:,.0f}" if pd.notna(pay_total) else "N/A")

k5, k6 = st.columns(2)
k5.metric("❓ Pembayaran Kosong", f"{miss_pay:,.0f}")
k6.metric("❓ Tap-out Kosong",    f"{miss_tap:,.0f}")

st.divider()

# ═══════════════════════════════════════════════
#  TABS
# ═══════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Ikhtisar", "🛣️ Koridor", "⏱️ Durasi", "💳 Pembayaran", "🔍 Kualitas Data"
])

# ── IKHTISAR ──────────────────────────────────
with tab1:
    st.subheader("📈 Tren Transaksi Harian")
    daily = view.dropna(subset=["Tanggal"]).groupby("Tanggal")["transID"].count().sort_index()
    if not daily.empty:
        fig, ax = plt.subplots(figsize=(12, 4))
        apply_style(fig, ax)
        x = list(range(len(daily)))
        ax.fill_between(x, daily.values, alpha=0.15, color=BLUE)
        ax.plot(x, daily.values, marker="o", linewidth=2.3, color=BLUE,
                markerfacecolor=YELLOW, markeredgecolor=BLUE, markersize=7, zorder=5)
        ax.set_xticks(x)
        ax.set_xticklabels([str(d) for d in daily.index],
                           rotation=45, ha="right", fontsize=8.5, color=GRAY_MID)
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Jumlah Transaksi")
        ax.set_title("Jumlah Transaksi per Hari", color=NAVY, fontsize=13, fontweight="bold", pad=12)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Tidak ada tanggal valid.")
    st.caption("💡 Perhatikan tanggal dengan jumlah transaksi jauh lebih rendah.")

# ── KORIDOR ───────────────────────────────────
with tab2:
    st.subheader("🛣️ 10 Koridor dengan Transaksi Terbanyak")
    cc = valid_cor.groupby("corridorName")["transID"].count().sort_values(ascending=False).head(10)
    if not cc.empty:
        sc = cc.sort_values()
        n  = len(sc)
        cm = safe_cmap("YlGnBu")
        clrs = [cm(0.35 + 0.6 * i / max(n - 1, 1)) for i in range(n)]

        fig, ax = plt.subplots(figsize=(11, 5))
        apply_style(fig, ax)
        ax.barh(range(n), sc.values, color=clrs, edgecolor="white", linewidth=0.8, height=0.62)
        for i, v in enumerate(sc.values):
            ax.text(v + sc.values.max() * 0.01, i, f"{v:,}",
                    va="center", ha="left", color=NAVY, fontsize=8.5, fontweight="600")
        ax.set_yticks(range(n))
        ax.set_yticklabels(sc.index, fontsize=8.5, color=GRAY_DARK)
        ax.set_xlabel("Jumlah Transaksi")
        ax.set_title("Top 10 Koridor — Volume Transaksi", color=NAVY, fontsize=13, fontweight="bold", pad=12)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.dataframe(cc.rename("Jumlah Transaksi").to_frame(), use_container_width=True)
    else:
        st.info("Tidak ada nama koridor valid.")

# ── DURASI ────────────────────────────────────
with tab3:
    st.subheader("⏱️ 10 Koridor dengan Rata-rata Durasi Terlama")
    dd = view[view["corridorName"].notna() & view["corridorName"].ne("") &
              view["Durasi_Menit"].notna() & (view["Durasi_Menit"] >= 0)]
    dbc = (dd.groupby("corridorName")
             .agg(Jumlah_Transaksi=("transID","count"),
                  Rata_rata_Durasi=("Durasi_Menit","mean"),
                  Median_Durasi=("Durasi_Menit","median"))
             .sort_values("Rata_rata_Durasi", ascending=False))
    td = dbc.head(10)
    if not td.empty:
        st_d = td["Rata_rata_Durasi"].sort_values()
        n = len(st_d)
        cm2 = safe_cmap("Blues")
        clrs2 = [cm2(0.35 + 0.6 * i / max(n - 1, 1)) for i in range(n)]

        fig, ax = plt.subplots(figsize=(11, 5))
        apply_style(fig, ax)
        ax.barh(range(n), st_d.values, color=clrs2, edgecolor="white", linewidth=0.8, height=0.62)
        for i, v in enumerate(st_d.values):
            ax.text(v + st_d.values.max() * 0.01, i, f"{v:.1f} mnt",
                    va="center", ha="left", color=NAVY, fontsize=8.5, fontweight="600")
        ax.set_yticks(range(n))
        ax.set_yticklabels(st_d.index, fontsize=8.5, color=GRAY_DARK)
        ax.set_xlabel("Rata-rata Durasi (menit)")
        ax.set_title("Top 10 Koridor — Rata-rata Durasi", color=NAVY, fontsize=13, fontweight="bold", pad=12)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.dataframe(td.round(2), use_container_width=True)
    else:
        st.info("Belum ada durasi valid.")
    st.caption("💡 Durasi lebih lama tidak otomatis berarti kemacetan; panjang rute juga memengaruhi.")

# ── PEMBAYARAN ────────────────────────────────
with tab4:
    st.subheader("💳 Transaksi Berdasarkan Kategori Pembayaran")
    bd = view[view["payCardBank"].notna() & view["payCardBank"].ne("")]
    bs = (bd.groupby("payCardBank")
            .agg(Jumlah_Transaksi=("transID","count"),
                 Total_Pembayaran=("payAmount","sum"),
                 Pembayaran_Kosong=("payAmount", lambda x: x.isna().sum()))
            .sort_values("Jumlah_Transaksi", ascending=False))
    if not bs.empty:
        col_a, col_b = st.columns([3, 2])

        with col_a:
            sb = bs["Jumlah_Transaksi"].sort_values()
            n = len(sb)
            bc = [BLUE if i % 2 == 0 else YELLOW for i in range(n)]
            fig, ax = plt.subplots(figsize=(8, max(3, n * 0.78)))
            apply_style(fig, ax)
            ax.barh(range(n), sb.values, color=bc, edgecolor="white", linewidth=0.8, height=0.6)
            for i, v in enumerate(sb.values):
                tc = NAVY if bc[i] == YELLOW else WHITE
                ax.text(v * 0.97, i, f"{v:,}", va="center", ha="right",
                        color=tc, fontsize=8.5, fontweight="700")
            ax.set_yticks(range(n))
            ax.set_yticklabels(sb.index, fontsize=9, color=GRAY_DARK)
            ax.set_xlabel("Jumlah Transaksi")
            ax.set_title("Volume per Bank", color=NAVY, fontsize=11, fontweight="bold", pad=10)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with col_b:
            t5 = bs["Jumlah_Transaksi"].head(5)
            pc = [BLUE, YELLOW, SKY, GOLD, NAVY]
            fig2, ax2 = plt.subplots(figsize=(5, 5))
            fig2.patch.set_facecolor(WHITE)
            ax2.set_facecolor(WHITE)
            wedges, texts, autos = ax2.pie(
                t5.values, labels=t5.index, colors=pc,
                autopct="%1.1f%%", startangle=140,
                wedgeprops={"edgecolor": WHITE, "linewidth": 2.5},
                textprops={"color": GRAY_DARK, "fontsize": 8.5})
            for a in autos:
                a.set_fontweight("bold")
                a.set_color(GRAY_DARK)
            ax2.set_title("Distribusi Top 5", color=NAVY, fontsize=11, fontweight="bold")
            fig2.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)

        st.dataframe(bs, use_container_width=True)
    else:
        st.info("Tidak ada kategori pembayaran valid.")

# ── KUALITAS DATA ─────────────────────────────
with tab5:
    st.subheader("🔍 Pemeriksaan Kualitas Data")
    quality = pd.DataFrame({
        "Indikator": [
            "Total baris pada filter", "ID transaksi duplikat",
            "Pembayaran kosong", "Waktu tap-in kosong",
            "Waktu tap-out kosong", "Durasi negatif",
            "Baris gagal dibaca saat impor"
        ],
        "Jumlah": [
            len(view), view["transID"].duplicated().sum(),
            view["payAmount"].isna().sum(), view["tapInTime"].isna().sum(),
            view["tapOutTime"].isna().sum(), (view["Durasi_Menit"] < 0).sum(),
            len(failed_rows)
        ]
    })

    def badge(v, lbl):
        if lbl == "Total baris pada filter": return "✅ OK"
        if v == 0:  return "✅ Bersih"
        if v < 100: return "⚠️ Perlu cek"
        return "🔴 Perlu tindakan"

    quality["Status"] = [badge(r["Jumlah"], r["Indikator"]) for _, r in quality.iterrows()]
    st.dataframe(quality, use_container_width=True)

    fig, ax = plt.subplots(figsize=(9, 3.2))
    apply_style(fig, ax)
    iss = quality[quality["Indikator"] != "Total baris pada filter"].copy()
    bc2 = [DANGER if v > 100 else WARN_CLR if v > 0 else SUCCESS for v in iss["Jumlah"]]
    ax.barh(iss["Indikator"], iss["Jumlah"], color=bc2, edgecolor="white", linewidth=0.8, height=0.55)
    ax.set_xlabel("Jumlah")
    ax.set_title("Ringkasan Isu Kualitas Data", color=NAVY, fontsize=11, fontweight="bold", pad=10)
    patches = [
        mpatches.Patch(color=DANGER,  label="> 100 — Perlu tindakan"),
        mpatches.Patch(color=WARN_CLR, label="1–100 — Perlu cek"),
        mpatches.Patch(color=SUCCESS,  label="0 — Bersih"),
    ]
    ax.legend(handles=patches, loc="lower right", facecolor=WHITE,
              edgecolor=GRAY_LIGHT, labelcolor=GRAY_DARK, fontsize=8.5)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.warning("⚠️ Nilai kosong tidak otomatis dihapus. Interpretasi analisis harus menyebutkan keterbatasan data.")

# ═══════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════
st.divider()
foot = (
    '<div style="text-align:center;padding:10px 0 20px;color:#64748B;font-size:0.82rem;">'
    '🚌 Dashboard dibuat dengan '
    '<strong style="color:#1A56DB;">Python</strong> · '
    '<strong style="color:#0D2B6E;">Streamlit</strong> · '
    '<strong style="color:#1A56DB;">Pandas</strong> · '
    '<strong style="color:#F59E0B;">Matplotlib</strong>'
    ' &nbsp;|&nbsp; 🏙️ Tema TransJakarta</div>'
)
st.markdown(foot, unsafe_allow_html=True)
