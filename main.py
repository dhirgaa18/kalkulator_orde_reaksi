import streamlit as st
import pandas as pd
import math
from fractions import Fraction

# Konfigurasi halaman
st.set_page_config(page_title="Penentu Orde Reaksi", layout="wide")
st.title("🧪 Penentuan Orde Reaksi - Step by Step Wizard")

# Fungsi bantu untuk format orde sebagai pecahan + desimal
def format_orde_mixed(value):
    if value == int(value):
        return str(int(value))
    else:
        frac = Fraction(value).limit_denominator(10)
        return f"\\frac{{{frac.numerator}}}{{{frac.denominator}}} \\; (={round(value, 2)})"

# DATA DEFAULT
data_default = pd.DataFrame({
    '[A] (M)': [0.4, 0.8, 0.8],
    '[B] (M)': [0.2, 0.2, 0.8],
    'Laju (v)': [10, 20, 40],
})
data_default.insert(0, "No", range(1, len(data_default) + 1))

# LANGKAH 1: Input Data
st.header("⿡ Masukkan Data Percobaan")
st.write("Silakan masukkan konsentrasi reaktan dan laju reaksi dari beberapa eksperimen.")

data = st.data_editor(data_default, num_rows="dynamic", use_container_width=True, key="data_input")

if len(data) < 2:
    st.warning("Masukkan minimal 2 baris data untuk melanjutkan.")
    st.stop()

row_numbers = data["No"].tolist()

# LANGKAH 2: Orde terhadap A
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
        st.latex(r"\frac{v_2}{v_1} = \left( \frac{[A]_2}{[A]_1} \right)^x \left( \frac{[B]_2}{[B]_1} \right)^y")

        A1, A2 = d1['[A] (M)'], d2['[A] (M)']
        B1, B2 = d1['[B] (M)'], d2['[B] (M)']
        v1, v2 = d1['Laju (v)'], d2['Laju (v)']

        ratio_v = v2 / v1
        ratio_A = A2 / A1

        st.header("⿤ Substitusi Nilai")
        st.latex(
            rf"\frac{{{v2}}}{{{v1}}} = "
            rf"\left( \frac{{{A2}}}{{{A1}}} \right)^x "
            rf"\cancel{{\left( \frac{{{B2}}}{{{B1}}} \right)^y}}"
        )

        try:
            x_value = math.log(ratio_v) / math.log(ratio_A)
            x = round(x_value, 6)
            st.latex(rf"x = {format_orde_mixed(x)}")
        except:
            st.error("⚠ Terjadi kesalahan saat menghitung orde terhadap A.")

# LANGKAH 3: Orde terhadap B
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
        st.latex(r"\frac{v_2}{v_1} = \left( \frac{[A]_2}{[A]_1} \right)^x \left( \frac{[B]_2}{[B]_1} \right)^y")

        A1, A2 = d1['[A] (M)'], d2['[A] (M)']
        B1, B2 = d1['[B] (M)'], d2['[B] (M)']
        v1, v2 = d1['Laju (v)'], d2['Laju (v)']

        ratio_v = v2 / v1
        ratio_B = B2 / B1

        st.header("⿩ Substitusi Nilai")
        st.latex(
            rf"\frac{{{v2}}}{{{v1}}} = "
            rf"\cancel{{\left( \frac{{{A2}}}{{{A1}}} \right)^x}} "
            rf"\left( \frac{{{B2}}}{{{B1}}} \right)^y"
        )

        try:
            y_value = math.log(ratio_v) / math.log(ratio_B)
            y = round(y_value, 6)
            st.latex(rf"y = {format_orde_mixed(y)}")
        except:
            st.error("⚠ Terjadi kesalahan saat menghitung orde terhadap B.")

# LANGKAH 4: Total Orde
if x is not None and y is not None:
    st.divider()
    st.header("📊 Orde Total Reaksi")
    total_order = x + y

    st.latex(
        rf"\text{{Orde total reaksi adalah }} x + y = {format_orde_mixed(x)} + {format_orde_mixed(y)} = {format_orde_mixed(total_order)}"
    )

    st.markdown("""
    <br>
    <hr>
    <b>📘 Penjelasan Rumus:</b><br>
    Jika <strong>[B]</strong> tetap, maka orde terhadap <strong>A</strong> dihitung dengan:<br><br>

    $$
    \\frac{v_2}{v_1} = \\left( \\frac{[A]_2}{[A]_1} \\right)^x
    $$

    Maka:

    $$
    x = \\frac{\\log(v_2/v_1)}{\\log([A]_2/[A]_1)}
    $$

    Jika <strong>[A]</strong> tetap, maka orde terhadap <strong>B</strong> dihitung dengan:<br><br>

    $$
    \\frac{v_2}{v_1} = \\left( \\frac{[B]_2}{[B]_1} \\right)^y
    $$

    Maka:

    $$
    y = \\frac{\\log(v_2/v_1)}{\\log([B]_2/[B]_1)}
    $$
    """, unsafe_allow_html=True)
