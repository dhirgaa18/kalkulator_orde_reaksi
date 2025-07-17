import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

st.set_page_config(page_title="Regresi Orde Reaksi", layout="centered")
st.title("Analisis Orde Reaksi Berdasarkan Data Konsentrasi vs Waktu")

st.markdown("""
Masukkan data waktu (t) dan konsentrasi atau absorbansi (A) pada tabel berikut. Aplikasi ini akan menampilkan grafik dan analisis regresi untuk orde 0, 1, dan 2 berdasarkan persamaan kinetika reaksi.

- *Orde 0:* A = A₀ - kt
- *Orde 1:* ln A = ln A₀ - kt
- *Orde 2:* 1/A = kt + 1/A₀
""")

# Tabel input data
default_data = pd.DataFrame({
    't': [0, 1, 2, 3, 4, 5],
    'A': [10, 8.4, 7.1, 5.9, 4.8, 3.6]
})
data = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

# Validasi data
if len(data.dropna()) >= 2:
    try:
        t = data['t'].astype(float).to_numpy()
        A = data['A'].astype(float).to_numpy()

        selected_orders = st.multiselect(
            "Pilih orde reaksi untuk dianalisis:",
            options=[0, 1, 2],
            default=[0, 1, 2],
            format_func=lambda x: f"Orde {x}"
        )

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['red', 'green', 'blue']

        for i, order in enumerate(selected_orders):
            if order == 0:
                X = t.reshape(-1, 1)
                Y = A
                label = "Orde 0: A vs t"
            elif order == 1:
                if np.any(A <= 0):
                    st.warning("Terdapat nilai A <= 0, tidak bisa dihitung ln(A) untuk orde 1.")
                    continue
                X = t.reshape(-1, 1)
                Y = np.log(A)
                label = "Orde 1: ln A vs t"
            elif order == 2:
                if np.any(A <= 0):
                    st.warning("Terdapat nilai A <= 0, tidak bisa dihitung 1/A untuk orde 2.")
                    continue
                X = t.reshape(-1, 1)
                Y = 1 / A
                label = "Orde 2: 1/A vs t"

            model = LinearRegression()
            model.fit(X, Y)
            Y_pred = model.predict(X)
            r2 = r2_score(Y, Y_pred)

            ax.plot(t, Y, 'o', color=colors[i], label=label + f"\nR² = {r2:.4f}")
            ax.plot(t, Y_pred, '-', color=colors[i], label=f"Fit Orde {order}: y = {model.coef_[0]:.4f}t + {model.intercept_:.4f}")

        ax.set_xlabel("Waktu (t)")
        ax.set_ylabel("Transformasi A sesuai orde")
        ax.set_title("Regresi Kinetika Reaksi Kimia")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data: {e}")
else:
    st.warning("Masukkan minimal dua baris data valid.")
