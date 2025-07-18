import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

st.set_page_config(page_title="Multi Halaman", layout="wide")

st.sidebar.title("📂 Navigasi")
page = st.sidebar.selectbox("Pilih Halaman", ["Beranda", "Analisis Orde", "Grafik Regresi"])

if page == "Beranda":
    st.title("📊 Aplikasi Kinetika Reaksi")
    st.markdown("Selamat datang! Silakan pilih menu di sidebar.")
    
elif page == "Analisis Orde":
    st.title("⚗️ Analisis Orde Reaksi")
    # (paste kode analisis orde dari sebelumnya di sini)

elif page == "Grafik Regresi":
    st.title("📈 Grafik Regresi dari Tabel")
    # (paste kode regresi tabel dari sebelumnya di sini)

st.set_page_config(page_title="Kinetika Reaksi", layout="centered")
st.title("🔬 Analisis Orde Reaksi Berdasarkan Data Waktu dan Konsentrasi")

st.markdown("""
Masukkan data waktu dan konsentrasi. Program ini akan menghitung regresi linier berdasarkan model kinetika reaksi:

- **Orde 0** → [A] vs waktu  
- **Orde 1** → ln[A] vs waktu  
- **Orde 2** → 1/[A] vs waktu

Kemudian akan menampilkan model terbaik berdasarkan nilai R² tertinggi.
""")

# Tabel input
default_data = pd.DataFrame({
    'Waktu': [],
    'Konsentrasi': []
})
data = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

if len(data.dropna()) >= 2:
    try:
        waktu = data['Waktu'].astype(float).to_numpy()
        konsentrasi = data['Konsentrasi'].astype(float).to_numpy()

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
                best_equation = f"{label} = {intercept:.4f} + {slope:.4f}·waktu"

            # Plot data dan fit
            ax.plot(waktu, y_trans, 'o', color=colors[order], label=f"Orde {order} Data")
            ax.plot(waktu, y_pred, '-', color=colors[order], label=f"Orde {order} Fit (R² = {r2:.4f})")

            # Tampilkan persamaan
            st.markdown(f"""
            ### Orde {order}
            Transformasi: `{label} = {intercept:.4f} + {slope:.4f}·waktu`  
            R² = `{r2:.4f}`
            """)

        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        # Hasil terbaik
        if best_order is not None:
            st.success(f"✅ **Orde terbaik adalah Orde {best_order}** dengan R² = `{best_r2:.4f}`")
            st.markdown(f"**Model terbaik:** `{best_equation}`")

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memproses data: {e}")
else:
    st.warning("⚠️ Masukkan setidaknya dua pasang data valid.")
