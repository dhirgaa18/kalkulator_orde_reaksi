import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

st.set_page_config(page_title="Kinetika Reaksi", layout="centered")
st.title("🔬 Analisis Orde Reaksi (dengan Koma Desimal)")

st.markdown("""
Masukkan data waktu dan konsentrasi di bawah.  
Gunakan **koma** untuk pemisah desimal (misalnya: `0,5` untuk 0.5).

Model regresi:
- **Orde 0** → [A] vs waktu  
- **Orde 1** → ln[A] vs waktu  
- **Orde 2** → 1/[A] vs waktu
""")

# Tabel input: sebagai teks agar koma bisa ditangani
default_data = pd.DataFrame({
    'Waktu': ['0', '1', '2', '3', '4'],
    'Konsentrasi': ['0,50', '0,40', '0,31', '0,25', '0,20']
})
data = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

# Fungsi konversi string dengan koma ke float
def parse_comma(series):
    return series.astype(str).str.replace(',', '.').astype(float)

# Fungsi format hasil angka dengan koma
def fmt_koma(val, ndigits=4):
    return str(round(val, ndigits)).replace('.', ',')

if len(data.dropna()) >= 2:
    try:
        waktu = parse_comma(data['Waktu'])
        konsentrasi = parse_comma(data['Konsentrasi'])

        selected_orders = st.multiselect(
            "Pilih orde reaksi yang ingin dianalisis:",
            options=[0, 1, 2],
            default=[0, 1, 2]
        )

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title("Regresi Kinetika Reaksi")
        ax.set_xlabel("Waktu")
        ax.set_ylabel("Transformasi Konsentrasi")

        colors = {0: "blue", 1: "green", 2: "red"}
        best_r2 = -np.inf
        best_order = None
        best_equation = ""

        for order in selected_orders:
            if order == 0:
                y_trans = konsentrasi
                label = "[A]"
            elif order == 1:
                if np.any(konsentrasi <= 0):
                    st.warning("⚠️ ln(konsentrasi) tidak bisa dihitung untuk nilai ≤ 0.")
                    continue
                y_trans = np.log(konsentrasi)
                label = "ln[A]"
            elif order == 2:
                if np.any(konsentrasi == 0):
                    st.warning("⚠️ 1/konsentrasi tidak bisa dihitung untuk nilai = 0.")
                    continue
                y_trans = 1 / konsentrasi
                label = "1/[A]"
            else:
                continue

            # Regresi linier
            coeffs = np.polyfit(waktu, y_trans, 1)
            slope, intercept = coeffs
            y_pred = slope * waktu + intercept
            r2 = r2_score(y_trans, y_pred)

            # Cek terbaik
            if r2 > best_r2:
                best_r2 = r2
                best_order = order
                best_equation = f"{label} = {fmt_koma(intercept)} + {fmt_koma(slope)}·waktu"

            # Plot
            ax.plot(waktu, y_trans, 'o', color=colors[order], label=f"Orde {order} Data")
            ax.plot(waktu, y_pred, '-', color=colors[order], label=f"Orde {order} Fit (R² = {round(r2, 4)})")

            # Tampilkan hasil
            st.markdown(f"""
            ### Orde {order}
            Transformasi: `{label} = {fmt_koma(intercept)} + {fmt_koma(slope)}·waktu`  
            R² = `{fmt_koma(r2)}`
            """)

        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        # Output terbaik
        if best_order is not None:
            st.success(f"✅ Orde terbaik adalah **Orde {best_order}** dengan R² = `{fmt_koma(best_r2)}`")
            st.markdown(f"**Model terbaik:** `{best_equation}`")

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan: {e}")
else:
    st.warning("⚠️ Masukkan setidaknya dua baris data valid.")
