import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

st.set_page_config(page_title="Orde Reaction Calculator", layout="centered")
st.title("🧪 Orde Reaction Calculator")

st.markdown("""
Masukkan data **Waktu (X)** dan **Konsentrasi (Y)** melalui tabel di bawah ini. Kemudian pilih satu atau beberapa orde regresi
(orde 0 = konstan, orde 1 = linear, orde 2 = kuadratik, dst) yang ingin ditampilkan.
""")

# Tabel input
default_data = pd.DataFrame({
    'Waktu': [],
    'Konsentrasi': []
})
data = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

# Proses jika data cukup
if len(data.dropna()) >= 2:
    try:
        x = data['Waktu'].astype(float).to_numpy()
        y = data['Konsentrasi'].astype(float).to_numpy()

        # Pilih ordo regresi
        selected_orders = st.multiselect(
            "Pilih orde regresi yang ingin ditampilkan:",
            options=list(range(0, 6)),
            default=[1, 2]
        )

        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(x, y, color="black", label="Data Asli")

        x_linspace = np.linspace(x.min(), x.max(), 200)
        orders_mendekati_1 = []

        for order in selected_orders:
            coeffs = np.polyfit(x, y, deg=order)
            poly_func = np.poly1d(coeffs)
            y_pred = poly_func(x)
            r2 = r2_score(y, y_pred)

            # Simpan jika R² mendekati 1
            if r2 >= 0.99:
                orders_mendekati_1.append((order, r2))

            ax.plot(x_linspace, poly_func(x_linspace), label=f"Orde {order} (R² = {r2:.4f})")

        ax.set_xlabel("Waktu")
        ax.set_ylabel("Konsentrasi")
        ax.set_title("Regresi Polinomial Konsentrasi vs Waktu")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        # Tampilkan catatan jika cocok mendekati 1
        if orders_mendekati_1:
            st.success("✅ Model berikut mendekati R² = 1:")
            for order, r2 in orders_mendekati_1:
                st.markdown(f"- **Orde {order}** dengan R² = `{r2:.4f}`")

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memproses data: {e}")
else:
    st.warning("⚠️ Masukkan setidaknya dua pasang data pada tabel.")
