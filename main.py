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
    st.session_state.edit_index = None  # reset edit

# Form tambah/edit
if st.session_state.show_form:
    st.markdown("### Tambah / Edit Data")

    waktu_default = 0.0
    konsentrasi_default = 0.0
    if st.session_state.edit_index is not None:
        data_lama = st.session_state.data_entries[st.session_state.edit_index]
        waktu_default = data_lama["Waktu"]
        konsentrasi_default = data_lama["Konsentrasi"]

    with st.form("form_input"):
        waktu = st.number_input("Waktu", min_value=0.0, format="%.2f", value=waktu_default)
        konsentrasi = st.number_input("Konsentrasi", min_value=0.0, format="%.4f", value=konsentrasi_default)
        simpan = st.form_submit_button("Simpan")

        if simpan:
            if st.session_state.edit_index is None:
                # Tambah baru
                st.session_state.data_entries.append({
                    "Waktu": waktu,
                    "Konsentrasi": konsentrasi
                })
                st.success("✅ Data berhasil ditambahkan.")
            else:
                # Edit data lama
                st.session_state.data_entries[st.session_state.edit_index] = {
                    "Waktu": waktu,
                    "Konsentrasi": konsentrasi
                }
                st.success("✏️ Data berhasil diperbarui.")
                st.session_state.edit_index = None

            st.session_state.show_form = False  # tutup form

# Tampilkan data sebagai tabel + tombol edit
if st.session_state.data_entries:
    st.markdown("### Data Tersimpan")
    
    # Header manual
    col1, col2, col3, col4 = st.columns([1, 2, 3, 1])
    col1.markdown("**No.**")
    col2.markdown("**Waktu**")
    col3.markdown("**Konsentrasi**")
    col4.markdown("**Aksi**")
    
    # Data per baris
    for i, entry in enumerate(st.session_state.data_entries):
        col1, col2, col3, col4 = st.columns([1, 2, 3, 1])
        col1.write(i + 1)
        col2.write(entry["Waktu"])
        col3.write(entry["Konsentrasi"])
        if col4.button("Edit", key=f"edit_{i}"):
            st.session_state.edit_index = i
            st.session_state.show_form = True
