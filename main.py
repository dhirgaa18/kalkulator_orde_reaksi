import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

st.set_page_config(page_title="Regresi Polinomial dari Tabel", layout="centered")
st.title("📈 Regresi Polinomial dan Korelasi dari Tabel Data")

st.markdown("""
Masukkan data Waktu (X) dan Konsentrasi (Y) melalui tabel di bawah ini. Kemudian pilih satu atau beberapa orde regresi
(orde 0 = konstan, orde 1 = linear, orde 2 = kuadratik, dst) yang ingin ditampilkan.
""")

# --- Tabel input data default
default_data = pd.DataFrame({
    'Waktu': [],
    'Konsentrasi': []
})

data = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

# Validasi data minimal
if len(data.dropna()) >= 2:
    try:
        x = data['X'].astype(float).to_numpy()
        y = data['Y'].astype(float).to_numpy()

        # Pilihan orde regresi
        selected_orders = st.multiselect(
            "Pilih orde regresi yang ingin ditampilkan:",
            options=list(range(0, 6)),
            default=[1, 2]
        )

        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(x, y, color="black", label="Data Asli")

        x_linspace = np.linspace(x.min(), x.max(), 200)

        for order in selected_orders:
            coeffs = np.polyfit(x, y, deg=order)
            poly_func = np.poly1d(coeffs)
            y_pred = poly_func(x)
            r2 = r2_score(y, y_pred)

            # Gambar garis regresi
            ax.plot(x_linspace, poly_func(x_linspace), label=f"Orde {order} (R² = {r2:.4f})")

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Regresi Polinomial")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data: {e}")
else:
    st.warning("⚠️ Masukkan setidaknya dua pasang data pada tabel.")
