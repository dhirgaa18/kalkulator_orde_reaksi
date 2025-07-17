import streamlit as st

st.title("Orde Reaction Calculator")

# Inisialisasi session state
if "data_entries" not in st.session_state:
    st.session_state.data_entries = []
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# Tambah data baru
with st.form("form_tambah"):
    st.subheader("Tambah Data Baru")
    waktu_baru = st.number_input("Waktu", min_value=0.0, format="%.2f")
    kons_baru = st.number_input("Konsentrasi", min_value=0.0, format="%.4f")
    if st.form_submit_button("Simpan"):
        st.session_state.data_entries.append({
            "Waktu": waktu_baru,
            "Konsentrasi": kons_baru
        })
        st.success("✅ Data ditambahkan.")

# Tampilkan tabel dengan tombol edit dan form edit lokal
if st.session_state.data_entries:
    st.subheader("Data Tersimpan")
    
    col_head1, col_head2, col_head3, col_head4 = st.columns([1, 2, 3, 2])
    col_head1.markdown("**No.**")
    col_head2.markdown("**Waktu**")
    col_head3.markdown("**Konsentrasi**")
    col_head4.markdown("**Aksi**")
    
    for i, entry in enumerate(st.session_state.data_entries):
        col1, col2, col3, col4 = st.columns([1, 2, 3, 2])
        col1.write(i + 1)
        col2.write(entry["Waktu"])
        col3.write(entry["Konsentrasi"])
        
        if st.session_state.edit_index == i:
            with col4.form(f"form_edit_{i}"):
                new_waktu = st.number_input("Waktu", value=entry["Waktu"], key=f"w_{i}")
                new_kons = st.number_input("Konsentrasi", value=entry["Konsentrasi"], key=f"k_{i}")
                simpan_edit = st.form_submit_button("Simpan Perubahan")
                if simpan_edit:
                    st.session_state.data_entries[i] = {
                        "Waktu": new_waktu,
                        "Konsentrasi": new_kons
                    }
                    st.success(f"✅ Baris {i+1} berhasil diperbarui.")
                    st.session_state.edit_index = None
        else:
            if col4.button("Edit", key=f"edit_btn_{i}"):
                st.session_state.edit_index = i
