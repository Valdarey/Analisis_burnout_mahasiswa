import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ── Konfigurasi halaman ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analisis Dampak AI pada Mahasiswa",
    page_icon="",
    layout="wide"
)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    BASE = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(BASE, "ai_student_impact_dataset.csv"))
    return df.drop(columns=['Student_ID'])

df_ori = load_data()

# ── Mapping label ramah ───────────────────────────────────────────────────────
MAJOR_MAP = {
    'Semua' : 'Semua',
    'Seni & Desain' : 'Arts',
    'Bisnis & Manajemen' : 'Business',
    'Ilmu Sosial & Humaniora' : 'Humanities',
    'Kedokteran & Kesehatan' : 'Medical',
    'Sains & Teknologi (STEM)' : 'STEM',
}
YEAR_MAP = {
    'Semua' : 'Semua',
    'Tahun ke-1 (Freshman)' : 'Freshman',
    'Tahun ke-2 (Sophomore)' : 'Sophomore',
    'Tahun ke-3 (Junior)' : 'Junior',
    'Tahun ke-4 ' : 'Senior',
    'Pascasarjana ' : 'Graduate',
}
POLICY_MAP = {
    'Semua' : 'Semua',
    'AI Didorong Aktif' : 'Actively_Encouraged',
    'AI Boleh dengan Kutipan' : 'Allowed_With_Citation',
    'AI Dilarang Ketat' : 'Strict_Ban',
}

MAJOR_ORDER   = ['Arts', 'Business', 'Humanities', 'Medical', 'STEM']
YEAR_ORDER    = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
BURNOUT_ORDER = ['Low', 'Medium', 'High']
BURNOUT_LABEL = {'Low': 'Rendah', 'Medium': 'Sedang', 'High': 'Tinggi'}
BURNOUT_COLOR = ['#4CAF50', '#FF9800', '#F44336']
MAJOR_LABEL   = {v: k for k, v in MAJOR_MAP.items()  if v != 'Semua'}
YEAR_LABEL    = {v: k for k, v in YEAR_MAP.items()   if v != 'Semua'}

# ── Header ────────────────────────────────────────────────────────────────────
st.title("Analisis Dampak AI terhadap Mahasiswa")
st.caption("Dataset 50.000 mahasiswa · Filter interaktif · Visualisasi real-time")
st.divider()

# ── Sidebar Filter ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filter Data")

    pilih_major  = st.selectbox("Jurusan", list(MAJOR_MAP.keys()))
    pilih_year   = st.selectbox("Tahun Studi", list(YEAR_MAP.keys()))
    pilih_policy = st.selectbox("Kebijakan Kampus", list(POLICY_MAP.keys()))

    st.divider()
    st.caption("Pilih filter lalu hasil langsung diperbarui otomatis.")

# ── Filter data ───────────────────────────────────────────────────────────────
df = df_ori.copy()
if MAJOR_MAP[pilih_major]  != 'Semua': df = df[df['Major_Category'] == MAJOR_MAP[pilih_major]]
if YEAR_MAP[pilih_year]    != 'Semua': df = df[df['Year_of_Study'] == YEAR_MAP[pilih_year]]
if POLICY_MAP[pilih_policy]!= 'Semua': df = df[df['Institutional_Policy'] == POLICY_MAP[pilih_policy]]

if len(df) == 0:
    st.error("Tidak ada data untuk filter yang dipilih. Coba kombinasi lain.")
    st.stop()

# ── Statistik Ringkas ─────────────────────────────────────────────────────────
vc    = df['Burnout_Risk_Level'].value_counts()
total = len(df)

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total Mahasiswa", f"{total:,}")
col2.metric("Rata-rata GPA Awal", f"{df['Pre_Semester_GPA'].mean():.2f}")
col3.metric("Rata-rata GPA Akhir",f"{df['Post_Semester_GPA'].mean():.2f}")
col4.metric("Rata-rata Jam AI", f"{df['Weekly_GenAI_Hours'].mean():.1f} jam/minggu")
col5.metric("Burnout Tinggi", f"{vc.get('High', 0)/total*100:.1f}%")
col6.metric("Burnout Rendah", f"{vc.get('Low',  0)/total*100:.1f}%")

st.divider()

# ── Grafik ────────────────────────────────────────────────────────────────────

# Baris 1
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Distribusi Tingkat Burnout")
    vc_plot = vc.reindex(BURNOUT_ORDER, fill_value=0)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar([BURNOUT_LABEL[b] for b in BURNOUT_ORDER],
                  vc_plot.values, color=BURNOUT_COLOR, width=0.5)
    for bar, val in zip(bars, vc_plot.values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + max(vc_plot.values)*0.02,
                str(val), ha='center', fontsize=10, fontweight='bold')
    ax.set_ylabel('Jumlah Mahasiswa')
    ax.set_ylim(0, vc_plot.max() * 1.2)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_b:
    st.subheader("Burnout per Jurusan")
    pivot = df.groupby(['Major_Category','Burnout_Risk_Level']).size().unstack(fill_value=0)
    pivot = pivot.reindex(index=MAJOR_ORDER, columns=BURNOUT_ORDER, fill_value=0)
    pivot.index   = [MAJOR_LABEL.get(m, m) for m in pivot.index]
    pivot.columns = [BURNOUT_LABEL[b] for b in pivot.columns]
    fig, ax = plt.subplots(figsize=(6, 3.5))
    pivot.plot(kind='bar', ax=ax, color=BURNOUT_COLOR, alpha=0.85, width=0.7)
    ax.set_xlabel('')
    ax.set_ylabel('Jumlah')
    ax.legend(title='Burnout')
    ax.tick_params(axis='x', rotation=20)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

# Baris 2
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Burnout per Tahun Studi")
    pivot2 = df.groupby(['Year_of_Study','Burnout_Risk_Level']).size().unstack(fill_value=0)
    pivot2 = pivot2.reindex(index=YEAR_ORDER, columns=BURNOUT_ORDER, fill_value=0)
    pivot2.index   = [YEAR_LABEL.get(y, y) for y in pivot2.index]
    pivot2.columns = [BURNOUT_LABEL[b] for b in pivot2.columns]
    fig, ax = plt.subplots(figsize=(6, 3.5))
    pivot2.plot(kind='bar', ax=ax, color=BURNOUT_COLOR, alpha=0.85, width=0.7)
    ax.set_xlabel('')
    ax.set_ylabel('Jumlah')
    ax.legend(title='Burnout')
    ax.tick_params(axis='x', rotation=20)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_d:
    st.subheader("Rata-rata GPA Awal vs Akhir per Jurusan")
    gpa = df.groupby('Major_Category')[['Pre_Semester_GPA','Post_Semester_GPA']].mean()
    gpa = gpa.reindex(MAJOR_ORDER)
    gpa.index = [MAJOR_LABEL.get(m, m) for m in gpa.index]
    x = np.arange(len(gpa))
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.bar(x - 0.2, gpa['Pre_Semester_GPA'],  0.35, label='GPA Awal',  color='steelblue',  alpha=0.85)
    ax.bar(x + 0.2, gpa['Post_Semester_GPA'], 0.35, label='GPA Akhir', color='darkorange', alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(gpa.index, rotation=20, ha='right')
    ax.set_ylabel('GPA')
    ax.set_ylim(0, 4.2)
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

# Baris 3
col_e, col_f = st.columns(2)

with col_e:
    st.subheader("Rata-rata Jam Pemakaian AI per Minggu")
    genai = df.groupby(['Major_Category','Burnout_Risk_Level'])['Weekly_GenAI_Hours'].mean().unstack(fill_value=0)
    genai = genai.reindex(index=MAJOR_ORDER, columns=BURNOUT_ORDER, fill_value=0)
    genai.index   = [MAJOR_LABEL.get(m, m) for m in genai.index]
    genai.columns = [BURNOUT_LABEL[b] for b in genai.columns]
    fig, ax = plt.subplots(figsize=(6, 3.5))
    genai.plot(kind='bar', ax=ax, color=BURNOUT_COLOR, alpha=0.85, width=0.7)
    ax.set_xlabel('')
    ax.set_ylabel('Jam / Minggu')
    ax.legend(title='Burnout')
    ax.tick_params(axis='x', rotation=20)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_f:
    st.subheader("Korelasi Antar Faktor")
    num_cols   = ['Pre_Semester_GPA','Post_Semester_GPA','Weekly_GenAI_Hours',
                  'Traditional_Study_Hours','Perceived_AI_Dependency',
                  'Anxiety_Level_During_Exams','Skill_Retention_Score']
    label_cols = ['GPA Awal','GPA Akhir','Jam AI/Minggu',
                  'Belajar Mandiri','Ketergantungan AI',
                  'Kecemasan Ujian','Retensi Skill']
    corr = df[num_cols].corr()
    corr.index   = label_cols
    corr.columns = label_cols
    fig, ax = plt.subplots(figsize=(6, 4.5))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
                vmin=-1, vmax=1, ax=ax, annot_kws={'size': 8})
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── Tabel Data Mentah (opsional) ──────────────────────────────────────────────
st.divider()
with st.expander("Lihat Data Mentah"):
    st.dataframe(df.head(20000), use_container_width=True)
    st.caption(f"Menampilkan 20.000 dari {total:,} baris")
