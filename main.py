import streamlit as st
import pandas as pd
import math
from fractions import Fraction

st.set_page_config(page_title="Penentu Orde Reaksi", layout="wide")

# Sidebar Navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Beranda", "Penentuan Orde", "Petunjuk", "Hasil"])

# ================================
# 📌 BERANDA
# ================================
if page == "Beranda":
    st.title("🔬 Penentu Orde Reaksi")
    st.markdown("""
    Selamat datang!  
    Aplikasi ini membantu kamu menentukan *orde reaksi* terhadap A dan B berdasarkan data percobaan.

    Gunakan menu di sidebar untuk:
    - 📊 Menentukan Orde Reaksi
    - 📘 Melihat Petunjuk Penggunaan
    - 📈 Lihat Hasil & Analisis
    """)

# ================================
# 📌 PENENTUAN ORDE
# ================================
elif page == "Penentuan Orde":
    st.title("📊 Penentuan Orde Reaksi")

    # Data default
    data_default = pd.DataFrame({
        '[A] (M)': [],
        '[B] (M)': [],
        'Laju (v)': [],
    })

    data_default.insert(0, "No", range(1, len(data_default) + 1))

    st.header("Masukkan Data Percobaan")
    data = st.data_editor(data_default, num_rows="dynamic", use_container_width=True, key="data_input")

    if len(data) < 2:
        st.warning("Masukkan minimal 2 baris data untuk melanjutkan.")
        st.stop()

    nomor_baris = data["No"].tolist()

    # Orde terhadap A
    st.header("⿢ Pilih Data untuk Orde terhadap A")
    pair_A = st.multiselect("Pilih dua baris dengan [B] sama:", nomor_baris, default=[1, 2], key="select_pair_A")

    x_frac = None
    if len(pair_A) == 2:
        idx1, idx2 = sorted(pair_A)
        d1 = data[data["No"] == idx1].iloc[0]
        d2 = data[data["No"] == idx2].iloc[0]

        if d1['[B] (M)'] != d2['[B] (M)']:
            st.error("Nilai [B] harus sama.")
        else:
            v1, v2 = d1['Laju (v)'], d2['Laju (v)']
            A1, A2 = d1['[A] (M)'], d2['[A] (M)']
            ratio_v = max(v1, v2) / min(v1, v2)
            ratio_A = max(A1, A2) / min(A1, A2)

            try:
                x_val = math.log(ratio_v) / math.log(ratio_A)
                x_frac = Fraction(x_val).limit_denominator()
                st.success(f"Orde terhadap A = {x_frac} (≈ {x_val:.4f})")
            except Exception as e:
                st.error(f"Kesalahan: {e}")

    # Orde terhadap B
    st.header("⿣ Pilih Data untuk Orde terhadap B")
    pair_B = st.multiselect("Pilih dua baris dengan [A] sama:", nomor_baris, default=[1, 3], key="select_pair_B")

    y_frac = None
    if len(pair_B) == 2:
        idx1, idx2 = sorted(pair_B)
        d1 = data[data["No"] == idx1].iloc[0]
        d2 = data[data["No"] == idx2].iloc[0]

        if d1['[A] (M)'] != d2['[A] (M)']:
            st.error("Nilai [A] harus sama.")
        else:
            v1, v2 = d1['Laju (v)'], d2['Laju (v)']
            B1, B2 = d1['[B] (M)'], d2['[B] (M)']
            ratio_v = max(v1, v2) / min(v1, v2)
            ratio_B = max(B1, B2) / min(B1, B2)

            try:
                y_val = math.log(ratio_v) / math.log(ratio_B)
                y_frac = Fraction(y_val).limit_denominator()
                st.success(f"Orde terhadap B = {y_frac} (≈ {y_val:.4f})")
            except Exception as e:
                st.error(f"Kesalahan: {e}")

    # Orde total
    if x_frac is not None and y_frac is not None:
        total = x_frac + y_frac
        st.header("⿤ Orde Total Reaksi")
        st.success(f"Total Orde = {x_frac} + {y_frac} = {total} (≈ {float(total):.4f})")
        st.info(f"Persamaan laju: v = k [A]^{x_frac} [B]^{y_frac}")

# ================================
# 📌 PETUNJUK
# ================================
elif page == "Petunjuk":
    st.title("📘 Petunjuk Penggunaan")
    st.markdown("""
    ### Cara Menentukan Orde Reaksi
    1. Masukkan data konsentrasi dan laju reaksi
    2. Pilih dua percobaan:
       - [B] konstan untuk cari orde A
       - [A] konstan untuk cari orde B
    3. Aplikasi akan hitung orde dalam pecahan dan desimal

    ### Rumus:
    $$
    \\frac{v_2}{v_1} = \\left( \\frac{[A]_2}{[A]_1} \\right)^x \\left( \\frac{[B]_2}{[B]_1} \\right)^y
    $$
    """)

# ================================
# 📌 HASIL ANALISIS
# ================================
elif page == "Hasil":
    st.title("📈 Hasil & Analisis")
    st.markdown("""
    Di halaman ini kamu bisa:
    - Menampilkan grafik (belum tersedia)
    - Menyimpan hasil
    - Menganalisis tren perubahan laju reaksi

    🚧 Fitur tambahan bisa ditambahkan nanti.
    """)

