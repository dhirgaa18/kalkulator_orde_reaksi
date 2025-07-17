import streamlit as st
import pandas as pd

st.markdown("<h1 style='text-align: center;'>Orde Reaction Calculator</h1>", unsafe_allow_html=True)

# Inisialisasi
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "data_entries" not in st.session_state:
    st.session_state.data_entries = []
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# Tombol tambah data baru
if st.button("Tambahkan Data Baru"):
    st.session_state.show_form = True
    st.session_state.edit_index = None  # Reset edit mode

# Form input data
if st.session_state.show_form:
    st.markdown("### Tambah / Edit Data")
    
    # Jika sedang mengedit, ambil nilai sebelumnya
    waktu_default = 0.0
    konsentrasi_default = 0.0
    if st.session_state.edit_index is not None:
        data_lama = st.session_state.data_entries[st.session_state.edit_index]
        waktu_default = data_lama["Waktu"]
        konsentrasi_default = data_lama["Konsentrasi"]
    
    with st.form("form_data"):
        waktu = st.number_input("Waktu", min_value=0.0, format="%.2f", value=waktu_default)
        konsentrasi = st.number_input("Konsentrasi", min_value=0.0, format="%.4f", value=konsentrasi_default)
        simpan = st.form_submit_button("Simpan")
        
        if simpan:
            if st.session_state.edit_index is None:
                # Tambah data baru
                st.session_state.data_entries.append({
                    "Waktu": waktu,
                    "Konsentrasi": konsentrasi
                })
                st.success("✅ Data berhasil ditambahkan.")
            else:
                # Edit data yang ada
                st.session_state.data_entries[st.session_state.edit_index] = {
                    "Waktu": waktu,
                    "Konsentrasi": konsentrasi
                }
                st.success("✏️ Data berhasil diperbarui.")
                st.session_state.edit_index = None

            st.session_state.show_form = False  # Tutup form setelah simpan

# Tampilkan data dengan tombol edit
if st.session_state.data_entries:
    st.markdown("### Data yang Disimpan")
    
    df = pd.DataFrame(st.session_state.data_entries)
    st.dataframe(df, use_container_width=True)
    
    # Tombol edit per baris
    st.markdown("### Edit Baris")
    for i, row in enumerate(st.session_state.data_entries):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"{i+1}. Waktu: {row['Waktu']}, Konsentrasi: {row['Konsentrasi']}")
        with col2:
            if st.button("Edit", key=f"edit_{i}"):
                st.session_state.edit_index = i
                st.session_state.show_form = True
