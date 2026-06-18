# Analisis & Prediksi Dampak AI terhadap Mahasiswa

Project ini menganalisis bagaimana penggunaan AI Generatif (ChatGPT, Copilot, dll) mempengaruhi performa akademik dan kesehatan mental mahasiswa, serta membangun model **klasifikasi** untuk memprediksi tingkat risiko burnout.

🔗 **Live Demo:** [Lihat Dashboard Interaktif](https://rfenryhvy8bjickkcxddkh.streamlit.app/)

## Tentang Dataset

Dataset berisi **50.000 mahasiswa** dengan fitur:

| Fitur | Keterangan |
|---|---|
| `Major_Category` | Jurusan (Arts, Business, Humanities, Medical, STEM) |
| `Year_of_Study` | Tahun studi (Freshman - Graduate) |
| `Pre_Semester_GPA` / `Post_Semester_GPA` | GPA sebelum & sesudah semester |
| `Weekly_GenAI_Hours` | Jam pemakaian AI per minggu |
| `Tool_Diversity` | Jumlah variasi tools AI yang dipakai |
| `Primary_Use_Case` | Tujuan utama pemakaian AI |
| `Prompt_Engineering_Skill` | Tingkat skill prompt (Beginner - Advanced) |
| `Paid_Subscription` | Status berlangganan AI berbayar |
| `Traditional_Study_Hours` | Jam belajar mandiri per minggu |
| `Perceived_AI_Dependency` | Skor ketergantungan terhadap AI |
| `Institutional_Policy` | Kebijakan kampus terhadap AI |
| `Anxiety_Level_During_Exams` | Skor kecemasan saat ujian |
| `Skill_Retention_Score` | Skor retensi kemampuan/skill |
| `Burnout_Risk_Level` | **Target** — Low / Medium / High |

## Tujuan

Menjawab pertanyaan: *"Berdasarkan kebiasaan belajar dan penggunaan AI, apakah seorang mahasiswa berisiko mengalami burnout Rendah, Sedang, atau Tinggi?"*

## Tools & Library

- Python, Pandas, NumPy
- Scikit-learn (preprocessing, model, evaluasi)
- Matplotlib, Seaborn (visualisasi)
- Streamlit (dashboard interaktif)
- Joblib (simpan model)

## Model yang Dibandingkan

| Model | Accuracy | F1 Macro |
|---|---|---|
| Decision Tree | 43.3% | 43.3% |
| KNN | 47.6% | 47.7% |
| Random Forest | 52.7% | 52.5% |
| **Gradient Boosting** | **53.6%** | **53.7%** |

> **Catatan:** Akurasi ~53% pada kasus ini tergolong wajar — data perilaku manusia dengan 3 kelas yang saling tumpang tindih secara alami sulit diprediksi dengan akurasi tinggi. Semua model menunjukkan performa serupa, menandakan keterbatasan ada pada sinyal data, bukan pada pemilihan model.

## Insight Utama

Berdasarkan analisis korelasi dan feature importance:
- **Jam pemakaian GenAI per minggu** adalah faktor paling berkorelasi dengan tingkat burnout
- **Ketergantungan terhadap AI** dan **kecemasan saat ujian** juga berkontribusi signifikan
- **Jam belajar tradisional** yang lebih tinggi cenderung berasosiasi dengan burnout lebih rendah
- Variasi jumlah tools AI (`Tool_Diversity`) hampir tidak berpengaruh terhadap burnout


## 📈 Visualisasi

Project ini mencakup:
- Correlation matrix antar fitur numerik
- Distribusi tingkat burnout
- Perbandingan burnout berdasarkan jurusan & tahun studi
- Perbandingan performa 4 model klasifikasi
- Confusion matrix tiap model
- Feature importance

---

**Dibuat sebagai project pembelajaran Data Science — klasifikasi dengan Scikit-learn & dashboard interaktif dengan Streamlit.**
