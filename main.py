import streamlit as st

st.markdown("<h1 style='text-align: center;'>Orde Reaction Calculator</h1>", unsafe_allow_html=True)

if st.button("Tambahkan Data"):
    st.session_state.show_form = not st.session_state.show_form
    
if st.session_state.show_form:
    st.markdown("### Form Tambah Data")
    with st.form("form_tambah_data"):
        nama = st.text_input("Nama")
        umur = st.number_input("Umur", min_value=0, max_value=120)
        pekerjaan = st.selectbox("Pekerjaan", ["Pelajar", "Mahasiswa", "Karyawan", "Lainnya"])
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            st.success(f"✅ Data disimpan:\n- Nama: {nama}\n- Umur: {umur}\n- Pekerjaan: {pekerjaan}")
