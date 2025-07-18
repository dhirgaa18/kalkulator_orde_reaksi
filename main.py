import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from fractions import Fraction
import math

# Konfigurasi Halaman
st.set_page_config(page_title="Analisis Orde Reaksi", layout="wide")

# Navigasi Halaman
page = st.sidebar.selectbox("Navigasi", ["Beranda", "Input Data dan Grafik", "Penentu Orde Reaksi", "Petunjuk"])

# ================================
# 📌 Fungsi Bantu
# ================================
def format_orde_mixed(value):
    if value == int(value):
        return str(int(value))
    else:
        frac = Fraction(value).limit_denominator(10)
        return f"\\frac{{{frac.numerator}}}{{{frac.denominator}}} \\; (={round(value, 2)})"

# ================================
# 📍 BERANDA
# ================================
if page == "Beranda":
    st.title("📘 Aplikasi Analisis Orde Reaksi")
    st.markdown("""
    Selamat datang! Aplikasi ini membantu Anda menentukan orde reaksi dari data eksperimen kimia.

    Silakan pilih menu di sebelah kiri untuk mulai menggunakan.
    """)

# ================================
# 📊 INPUT DATA & GRAFIK REGRESI
# ================================
elif page == "Input Data dan Grafik":
    st.title("📊 Regresi Polinomial dan Grafik Transformasi")
    st.markdown("""
    Masukkan data waktu dan konsentrasi untuk melihat grafik transformasi:

    - Orde 0: [A] vs waktu
    - Orde 1: ln[A] vs waktu
    - Orde 2: 1/[A] vs waktu
    """)

    default_data = pd.DataFrame({
        'Waktu': [0, 1, 2, 3, 4],
        'Konsentrasi (M)': [0.50, 0.40, 0.33, 0.25, 0.20]
    })

    df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

    if len(df.dropna()) >= 2:
        t = df['Waktu'].to_numpy()
        A = df['Konsentrasi (M)'].to_numpy()

        fig, ax = plt.subplots(figsize=(8, 5))
        best_r2 = -1
        best_order = None

        for orde in [0, 1, 2]:
            if orde == 0:
                y = A
                label = "[A] vs waktu"
            elif orde == 1:
                y = np.log(A)
                label = "ln[A] vs waktu"
            elif orde == 2:
                y = 1 / A
                label = "1/[A] vs waktu"

            model = LinearRegression().fit(t.reshape(-1, 1), y)
            y_pred = model.predict(t.reshape(-1, 1))
            r2 = r2_score(y, y_pred)

            ax.plot(t, y_pred, label=f"Orde {orde} (R²={r2:.4f})")

            if r2 > best_r2:
                best_r2 = r2
                best_order = orde

        ax.scatter(t, A, label="Data Aktual", color='black')
        ax.set_xlabel("Waktu")
        ax.set_ylabel("Transformasi Konsentrasi")
        ax.legend()
        st.pyplot(fig)

        st.success(f"✅ Orde terbaik berdasarkan R²: Orde {best_order} (R² = {best_r2:.4f})")
    else:
        st.warning("Masukkan minimal dua data.")

# ================================
# 🔍 PENENTU ORDE REAKSI
# ================================
elif page == "Penentu Orde Reaksi":
    st.title("Penentuan Orde Reaksi")

    data_default = pd.DataFrame({
        '[A] (M)': [0.4, 0.8, 0.8],
        '[B] (M)': [0.2, 0.2, 0.8],
        'Laju (v)': [10, 20, 40],
    })

    data_default.insert(0, "No", range(1, len(data_default) + 1))
    data = st.data_editor(data_default, num_rows="dynamic", use_container_width=True, key="data_input")

    if len(data) < 2:
        st.warning("Masukkan minimal 2 baris data untuk melanjutkan.")
        st.stop()

    row_numbers = data["No"].tolist()

    # Orde terhadap A
    st.header("⿢ Pilih Baris untuk Menentukan Orde terhadap A")
    pair_A = st.multiselect("Pilih dua nomor baris (dengan B yang sama):", row_numbers, default=[1, 2])
    x = None

    if len(pair_A) == 2:
        idx1 = data.index[data["No"] == pair_A[0]][0]
        idx2 = data.index[data["No"] == pair_A[1]][0]
        d1, d2 = data.loc[idx1], data.loc[idx2]

        if d1['[B] (M)'] != d2['[B] (M)']:
            st.error("❌ Nilai B harus sama untuk menentukan orde terhadap A.")
        else:
            st.header("⿣ Rumus Lengkap Orde A")
            st.latex(r"\frac{v_2}{v_1} = \left( \frac{[A]_2}{[A]_1} \right)^x")

            A1, A2 = d1['[A] (M)'], d2['[A] (M)']
            v1, v2 = d1['Laju (v)'], d2['Laju (v)']

            try:
                x_value = math.log(v2 / v1) / math.log(A2 / A1)
                x = round(x_value, 6)
                st.latex(rf"x = {format_orde_mixed(x)}")
            except:
                st.error("⚠ Terjadi kesalahan saat menghitung orde terhadap A.")

    # Orde terhadap B
    st.divider()
    st.header("⿧ Pilih Baris untuk Menentukan Orde terhadap B")
    pair_B = st.multiselect("Pilih dua nomor baris (dengan A yang sama):", row_numbers, default=[1, 3])
    y = None

    if len(pair_B) == 2:
        idx1 = data.index[data["No"] == pair_B[0]][0]
        idx2 = data.index[data["No"] == pair_B[1]][0]
        d1, d2 = data.loc[idx1], data.loc[idx2]

        if d1['[A] (M)'] != d2['[A] (M)']:
            st.error("❌ Nilai A harus sama untuk menentukan orde terhadap B.")
        else:
            st.header("⿨ Rumus Lengkap Orde B")
            st.latex(r"\frac{v_2}{v_1} = \left( \frac{[B]_2}{[B]_1} \right)^y")

            B1, B2 = d1['[B] (M)'], d2['[B] (M)']
            v1, v2 = d1['Laju (v)'], d2['Laju (v)']

            try:
                y_value = math.log(v2 / v1) / math.log(B2 / B1)
                y = round(y_value, 6)
                st.latex(rf"y = {format_orde_mixed(y)}")
            except:
                st.error("⚠ Terjadi kesalahan saat menghitung orde terhadap B.")

    # Orde total
    if x is not None and y is not None:
        st.divider()
        st.header("📊 Orde Total Reaksi")
        st.latex(
            rf"\text{{Orde total reaksi adalah }} x + y = {format_orde_mixed(x)} + {format_orde_mixed(y)} = {format_orde_mixed(x + y)}"
        )

# ================================
# 📘 PETUNJUK
# ================================
elif page == "Petunjuk":
    st.title("📘 Petunjuk Penggunaan")
    st.markdown("""
    ### 📊 Cara Menentukan Orde Reaksi
    1. Masukkan data konsentrasi dan laju reaksi dari beberapa percobaan.
    2. Pilih dua percobaan:
       - Di mana [B] konstan → untuk menentukan orde terhadap A
       - Di mana [A] konstan → untuk menentukan orde terhadap B
    3. Aplikasi akan menghitung orde reaksi dalam bentuk pecahan dan desimal.

    ### 🧪 Rumus Penentuan Orde Reaksi

    Jika **[B] tetap**, maka orde terhadap A dihitung dengan:

    $$
    \frac{v_2}{v_1} = \left( \frac{[A]_2}{[A]_1} \right)^x
    $$

    Maka:

    $$
    x = \frac{\log(v_2/v_1)}{\log([A]_2/[A]_1)}
    $$

    Jika **[A] tetap**, maka orde terhadap B dihitung dengan:

    $$
    \frac{v_2}{v_1} = \left( \frac{[B]_2}{[B]_1} \right)^y
    $$

    Maka:

    $$
    y = \frac{\log(v_2/v_1)}{\log([B]_2/[B]_1)}
    $$
    """)
