import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import locale

# Gunakan lokal Indonesia untuk pemisah koma
locale.setlocale(locale.LC_NUMERIC, 'id_ID.UTF-8')

st.set_page_config(page_title="Kinetika Reaksi", layout="centered")
st.title("🔬 Analisis Orde Reaksi (Format Koma)")

st.markdown("""
Masukkan data waktu dan konsentrasi. Gunakan **koma (`,`) sebagai pemisah desimal**.  
Contoh: `0,5` → 0.5

Model regresi:
- **Orde 0** → [A] vs waktu  
- **Orde 1** → ln[A] vs waktu  
- **Orde 2** → 1/[A] vs waktu
""")

# Tabel input sebagai teks (agar bisa koma)
default_data = pd.DataFrame({
    'Waktu': ['0', '1', '2', '3', '4'],
    'Konsentrasi': ['0,50', '0,40', '0,31', '0,25', '0,20']
})
data = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

def parse_comma_column(series):
    """Ubah angka koma ke float"""
    return series.str.replace(",", ".", regex=False).astype(float)

if len(data.dropna()) >= 2:
    try:
        waktu = parse_comma_column(data['Waktu'])
        konsentrasi = parse_comma_column(data['Konsentrasi'])

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
                    st.warning("⚠️ Tidak dapat menghitung ln(Konsentrasi) karena ada nilai ≤ 0.")
                    continue
                y_trans = np.log(konsentrasi)
                label = "ln[A]"
            elif order == 2:
                if np.any(konsentrasi == 0):
                    st.warning("⚠️ Tidak dapat menghitung 1/Konsentrasi karena ada nilai = 0.")
                    continue
                y_trans = 1 / konsentrasi
                label = "1/[A]"
            else:
                continue

            coeffs = np.polyfit(waktu, y_trans, 1)
            slope, intercept = coeffs
            y_pred = slope * waktu + intercept
            r2 = r2_score(y_trans, y_pred)

            # Cek R² terbaik
            if r2 > best_r2:
                best_r2 = r2
                best_order = order
                best_equation = f"{label} = {locale.format_string('%.4f', intercept)} + {locale.format_string('%.4f', slope)}·waktu"

            # Plot
            ax.plot(waktu, y_trans, 'o', color=colors[order], label=f"Orde {order} Data")
            ax.plot(waktu, y_pred, '-', color=colors[order], label=f"Orde {order} Fit (R² = {r2:.4f})")

            # Tampilkan persamaan
            st.markdown(f"""
            ### Orde {order}
            Transformasi: `{label} = {locale.format_string('%.4f', intercept)} + {locale.format_string('%.4f', slope)}·waktu`  
            R² = `{locale.format_string('%.4f', r2)}`
            """)

        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        if best_order is not None:
            st.success(f"✅ **Orde terbaik adalah Orde {best_order}** dengan R² = `{locale.format_string('%.4f', best_r2)}`")
            st.markdown(f"**Model terbaik:** `{best_equation}`")

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memproses data: {e}")
else:
    st.warning("⚠️ Masukkan setidaknya dua pasang data valid.")
