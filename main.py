import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import math
from fractions import Fraction
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


st.set_page_config(page_title="Kinetika Reaksi", layout="wide")

# Sidebar Navigasi
st.sidebar.title("📂 Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["🏠Beranda", "📊Analisis Orde", "🧮Penentuan Orde", "📖Petunjuk", "📘Tentang"])

# ================================
# 📌 BERANDA
# ================================
if page == "🏠Beranda":
    st.title("📊 Aplikasi Kinetika Reaksi")
    st.markdown("""
### Selamat datang di Aplikasi Kinetika Reaksi!

Aplikasi ini dirancang untuk membantu kamu menganalisis data eksperimen reaksi kimia secara cepat dan akurat. Kamu bisa:

- 📉 Menganalisis orde reaksi berdasarkan data
- 🧪 Menghitung orde berdasarkan percobaan
- 📈 Menampilkan grafik regresi transformasi konsentrasi
- 📘 Membaca panduan interaktif

""")
    st.success("👩‍🔬 Siap Menghitung Orde Reaksi!")
    st.info("📂 Gunakan menu navigasi di sebelah kiri untuk mulai.")

# ================================
# ⚗️ ANALISIS ORDE KINETIKA
# ================================
elif page == "📊Analisis Orde":
    st.title("🔬 Analisis Orde Reaksi Berdasarkan Data Waktu dan Konsentrasi")

    st.markdown("""
    Masukkan data waktu dan konsentrasi. Program ini akan menghitung regresi linier berdasarkan model kinetika reaksi:

    - **Orde 0** → [A] vs waktu  
    - **Orde 1** → ln[A] vs waktu  
    - **Orde 2** → 1/[A] vs waktu

    Kemudian akan menampilkan model terbaik berdasarkan nilai R² tertinggi.
    """)

    default_data = pd.DataFrame({'Waktu': [], 'Konsentrasi': []})
    data = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

    slope = None
    best_order = None

    if len(data.dropna()) >= 2:
        try:
            waktu = data['Waktu'].astype(float).to_numpy()
            konsentrasi = data['Konsentrasi'].astype(float).to_numpy()

            selected_orders = st.multiselect("Pilih orde reaksi yang ingin dianalisis:", options=[0, 1, 2], default=[0, 1, 2])

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.set_title("Regresi Kinetika Reaksi")
            ax.set_xlabel("Waktu")
            ax.set_ylabel("Transformasi Konsentrasi")

            colors = {0: "blue", 1: "green", 2: "red"}
            best_r2 = -np.inf
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
                slope_tmp, intercept = coeffs
                y_pred = slope_tmp * waktu + intercept
                r2 = r2_score(y_trans, y_pred)

                if r2 > best_r2:
                    best_r2 = r2
                    best_order = order
                    slope = slope_tmp
                    best_equation = f"{label} = {intercept:.4f} + {slope:.4f}·waktu"

                ax.plot(waktu, y_trans, 'o', color=colors[order], label=f"Orde {order} Data")
                ax.plot(waktu, y_pred, '-', color=colors[order], label=f"Orde {order} Fit (R² = {r2:.4f})")

                st.markdown(f"""
                ### Orde {order}  
                Transformasi: `{label} = {intercept:.4f} + {slope_tmp:.4f}·waktu`  
                R² = `{r2:.4f}`
                """)

            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

            if best_order is not None:
                st.success(f"✅ **Orde terbaik adalah Orde {best_order}** dengan R² = `{best_r2:.4f}`")
                st.markdown(f"**Model terbaik:** `{best_equation}`")

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat memproses data: {e}")
    else:
        st.warning("⚠️ Masukkan setidaknya dua pasang data valid.")

    if slope is not None and best_order is not None:
        st.subheader("⏳ Waktu Paruh dan Kadaluarsa")
        st.markdown("Perhitungan ini menggunakan nilai slope regresi sebagai konstanta laju reaksi `k`.")

        A0_input = st.number_input("Konsentrasi awal [A₀] (mol/L)", min_value=0.0, format="%.4f", value=0.0 if len(data.dropna()) == 0 else float(data['Konsentrasi'].iloc[0]))
        k_input = abs(slope)
        st.markdown(f"**Nilai k (konstanta laju)** diambil dari slope regresi: `k = {k_input:.6f}`")

        if k_input > 0 and (A0_input > 0 or best_order == 1):
            if best_order == 0:
                t_half = A0_input / (2 * k_input)
                t_90 = 0.1 * A0_input / k_input
            elif best_order == 1:
                t_half = math.log(2) / k_input
                t_90 = 0.105 / k_input
            elif best_order == 2:
                t_half = 1 / (k_input * A0_input)
                t_90 = 1 / (9 * k_input * A0_input)

            st.markdown("### 📉 Hasil Perhitungan:")
            st.latex(f"t_{{1/2}} = {t_half:.4f} \\, \\text{{(waktu agar [A] tinggal setengah)}}")
            st.latex(f"t_{{90}} = {t_90:.4f} \\, \\text{{(waktu agar [A] tinggal 10\\%)}}")
        else:
            st.warning("Masukkan nilai [A₀] > 0 (tidak boleh nol).")
# ================================
# 📌 PENENTUAN ORDE REAKSI
# ================================
elif page == "🧮Penentuan Orde":
    st.title("🧮Penentuan Orde Reaksi")

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

    if x_frac is not None and y_frac is not None:
        total = x_frac + y_frac
        st.header("⿤ Orde Total Reaksi")
        st.success(f"Total Orde = {x_frac} + {y_frac} = {total} (≈ {float(total):.4f})")
        st.info(f"Persamaan laju: v = k [A]^{x_frac} [B]^{y_frac}")

# ================================
# 📘 PETUNJUK
# ================================
elif page == "📖Petunjuk":
    st.title("📖Petunjuk Penggunaan")
    st.markdown(r"""
### Cara Menentukan Orde Reaksi
1. Masukkan data konsentrasi dan laju reaksi  
2. Pilih dua percobaan:
   - [B] konstan untuk cari orde A  
   - [A] konstan untuk cari orde B  
3. Aplikasi akan hitung orde dalam pecahan dan desimal  

### Rumus:
$$
\frac{v_2}{v_1} = \left( \frac{[A]_2}{[A]_1} \right)^x \left( \frac{[B]_2}{[B]_1} \right)^y
$$
""")

# ================================
# 📈 HASIL
# ================================
elif page == "Hasil":
    st.title("📈 Hasil & Analisis")
    st.markdown("""
### Di halaman ini kamu bisa:
- Menampilkan grafik (belum tersedia)
- Menyimpan hasil
- Menganalisis tren perubahan laju reaksi

🚧 Fitur tambahan bisa ditambahkan nanti.
""")

elif page == "📘Tentang":
    st.title("📘Tentang Kinetika Reaksi")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Tentang Website", "Dasar Teori", "Kontak", "Kritik dan Saran"])

    with tab1:
        st.subheader("Tentang Website")
        st.markdown("""
Aplikasi ini dikembangkan untuk membantu mahasiswa dan pelajar dalam memahami **kinetika reaksi** melalui pendekatan data eksperimen.  
Fitur yang tersedia antara lain:
- Analisis regresi untuk menentukan orde reaksi
- Penentuan orde reaksi berdasarkan data laju
- Perhitungan waktu paruh dan waktu kadaluarsa
- Visualisasi grafik transformasi konsentrasi

Website ini dibuat dengan **Streamlit**, menggunakan pustaka Python seperti `numpy`, `pandas`, `matplotlib`, dan `scikit-learn`.

**Aplikasi Ini Dikembangkan Oleh Kelompok 4 (1B)**
1. Affan Fakhri Izzudin
2. Dhirga Fayzul Haq
3. Laudya Calista Ardelia Ramadhani
4. Neha Atsana Putri Ahmad
5. Salma Nailah Putri
""")

    with tab2:
        st.header("🔬 Dasar Teori Kinetika Reaksi")
        st.markdown(r"""
Kinetika reaksi adalah cabang ilmu kimia yang mempelajari suatu reaksi kimia. Kinetika reaksi menerangkan dua hal yaitu mekanisme reaksi dan laju reaksi. Pengertian mekanisme reaksi adalah dipakai untuk menerangkan langkah-langkah dimana suatu reaktan menjadi produk. Laju reaksi adalah perubahan konsentrasi pereaksi ataupun suatu produk dalam suatu satuan waktu.

Laju menyatakan seberapa cepat atau seberapa lambat suatu proses berlangsung. Laju menyatakan besarnya perubahan yang terjadi dalam satu satuan waktu. Reaksi kimia adalah proses perubahan zat pereaksi menjadi produk. Seiring dengan bertambahnya waktu reaksi, maka jumlah zat pereaksi semakin sedikit, sedangkan produk semakin banyak. Laju reaksi dinyatakan sebagai laju berkurangnya pereaksi atau laju terbentuknya produk. Kecepatan reaksi kimia ditentukan oleh orde reaksi, yaitu jumlah dari eksponen konsentrasi pada persamaan kecepatan reaksi. Orde suatu reaksi ialah jumlah semua eksponen dari konsentrasi dalam persamaan laju. Orde reaksi juga menyatakan besarnya pengaruh konsentrasi reaktan (pereaksi) terhadap laju reaksi.

Dengan persamaan:

$$
v = k[A]^x[B]^y
$$

Di mana:
- \\( v \\) = laju reaksi  
- \\( k \\) = konstanta laju  
- \\( x, y \\) = orde reaksi terhadap A dan B  
- \\( [A], [B] \\) = konsentrasi reaktan  
""")

    with tab3:
        st.subheader("Kontak Pengembang")
        st.markdown("""
Jika ada pertanyaan, kritik, atau saran silakan hubungi:

📧 Email: `dhirgahaq18@gmail.com`  
🐙 GitHub: https://github.com/dhirgaa18  

Terima kasih telah menggunakan aplikasi ini! 🙌
""")
      
    with tab4:
        st.subheader("💬 Kritik dan Saran")
        st.markdown("Silakan berikan masukan atau komentar Anda di bawah ini:")
        
        nama = st.text_input("Nama")
        email = st.text_input("Email")
        pesan = st.text_area("Pesan")
    
        if st.button("Kirim"):
            if not nama or not email or not pesan:
                st.warning("Harap isi semua kolom terlebih dahulu.")
            else:
                try:
                    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
                    creds = ServiceAccountCredentials.from_json_keyfile_name("kritikdansaran-4b53109a0788.json", scope)
                    client = gspread.authorize(creds)

                    sheet = client.open("KritikSaranWeb").sheet1
                    sheet.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nama, email, pesan])
                    st.success("✅ Terima kasih! Kritik dan saranmu telah terkirim.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat mengirim: {e}")
