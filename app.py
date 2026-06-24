import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="Dashboard What-If Keuntungan Toko",
    page_icon="📊",
    layout="wide"
)

# =========================
# STYLE CUSTOM
# =========================
st.markdown("""
<style>

/* Background utama */
.stApp {
    background-color: #f4f7fc;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0f172a;
}

[data-testid="stSidebar"] * {
    color: white;
}

/* Judul */
.main-title {
    font-size: 42px;
    font-weight: bold;
    color: #1e40af;
}

/* Metric card langsung */
[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border-left: 6px solid #2563eb;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Header section */
h1, h2, h3 {
    color: #1e3a8a;
}

/* Table */
[data-testid="stTable"] {
    background-color: white;
    border-radius: 12px;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #2563eb;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LANGKAH 1: MODEL
# =========================
X_train = np.array([[5, 10], [10, 20], [15, 5], [20, 25], [25, 15]])
y_train = np.array([50, 80, 110, 90, 150])

model = LinearRegression().fit(X_train, y_train)

baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]

# =========================
# LANGKAH 2: SIMULASI
# =========================
def run_simulation(new_iklan, new_diskon):
    intervention_input = np.array([[new_iklan, new_diskon]])
    prediction = model.predict(intervention_input)[0]
    delta_y = prediction - baseline_pred
    return prediction, delta_y

# =========================
# LANGKAH 3: UI STREAMLIT
# =========================
st.markdown('<div class="main-title">📊 Simulator Kebijakan Keuntungan Toko</div>', unsafe_allow_html=True)
st.write("Aplikasi ini digunakan untuk mensimulasikan dampak perubahan **Anggaran Iklan** dan **Besaran Diskon** terhadap keuntungan toko.")

st.divider()

with st.sidebar:
    st.header("⚙️ Panel Intervensi")
    st.write("Atur nilai kebijakan toko di bawah ini.")

    iklan_slider = st.slider("💰 Anggaran Iklan (Juta)", 0, 50, 10)
    diskon_slider = st.slider("🏷️ Besaran Diskon (%)", 0, 50, 10)

    st.info("Baseline: Iklan 10 juta dan Diskon 10%")

hasil_pred, delta = run_simulation(iklan_slider, diskon_slider)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Baseline", f"Rp {baseline_pred:.2f} Jt")

with col2:
    st.metric("Prediksi Intervensi", f"Rp {hasil_pred:.2f} Jt")

with col3:
    st.metric("Perubahan Delta", f"{delta:.2f} Jt")

st.divider()

if delta > 0:
    st.success(f"Skenario ini meningkatkan keuntungan sebesar Rp {delta:.2f} juta dibandingkan baseline.")
elif delta < 0:
    st.error(f"Skenario ini menurunkan keuntungan sebesar Rp {abs(delta):.2f} juta dibandingkan baseline.")
else:
    st.info("Skenario ini menghasilkan keuntungan yang sama dengan baseline.")

# =========================
# FITUR UNIK: ASISTEN REKOMENDASI BISNIS
# =========================
st.subheader("🤖 Asisten Rekomendasi Bisnis")

target_keuntungan = 150
persentase_target = max(0, min(int((hasil_pred / target_keuntungan) * 100), 100))

st.markdown('<div class="unique-box">', unsafe_allow_html=True)

if hasil_pred >= 120 and delta > 0:
    status_bisnis = "Sangat Menguntungkan"
    rekomendasi = "Skenario ini sangat layak diterapkan karena keuntungan meningkat tinggi dan mendekati target bisnis."
elif hasil_pred >= 80 and delta >= 0:
    status_bisnis = "Cukup Menguntungkan"
    rekomendasi = "Skenario ini masih aman untuk dipertimbangkan karena tidak menurunkan keuntungan dari baseline."
elif delta < 0:
    status_bisnis = "Kurang Disarankan"
    rekomendasi = "Skenario ini sebaiknya tidak diterapkan karena menyebabkan penurunan keuntungan dibandingkan baseline."
else:
    status_bisnis = "Netral"
    rekomendasi = "Skenario ini menghasilkan keuntungan yang sama dengan kondisi awal."

st.write(f"**Status Bisnis:** {status_bisnis}")
st.write(f"**Rekomendasi:** {rekomendasi}")

st.write("**Progress Target Keuntungan:**")
st.progress(persentase_target)
st.write(f"Pencapaian target: **{persentase_target}%** dari target Rp {target_keuntungan} juta.")

st.divider()

data_plot = pd.DataFrame({
    "Skenario": ["Baseline", "Intervensi"],
    "Keuntungan": [baseline_pred, hasil_pred]
})

st.subheader("📈 Grafik Perbandingan Keuntungan")

chart = alt.Chart(data_plot).mark_bar(color="#2563eb").encode(
    x=alt.X(
        "Skenario:N",
        title="Skenario",
        axis=alt.Axis(labelAngle=0)
    ),
    y=alt.Y(
        "Keuntungan:Q",
        title="Keuntungan"
    ),
    tooltip=["Skenario", "Keuntungan"]
).properties(
    height=400
)

st.altair_chart(chart, use_container_width=True)

st.subheader("📋 Ringkasan Skenario")
st.table(pd.DataFrame({
    "Variabel": ["Anggaran Iklan", "Besaran Diskon", "Prediksi Keuntungan", "Delta", "Status Bisnis"],
    "Nilai": [
        f"{iklan_slider} Juta",
        f"{diskon_slider}%",
        f"Rp {hasil_pred:.2f} Juta",
        f"{delta:.2f} Juta",
        status_bisnis
    ]
}))