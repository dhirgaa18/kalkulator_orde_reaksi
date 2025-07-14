import streamlit as st

st.markdown("<h1 style='text-align: center;'>Orde Reaction Calculator</h1>", unsafe_allow_html=True)

if "show_form" not in st.session_state:
    st.session_state.show_form = False

if st.button("Tambahkan Data"):
    st.session_state.show_form = not st.session_state.show_form
    
if st.session_state.show_form:
    st.markdown("### Tambahkan Data Waktu dan Konsentrasi")
    with st.form("form_tambah_data"):
        waktu = st.number_input("Waktu", min_value= 0.0, format="%.2f")
        konsentrasi = st.number_input("Konsentrasi", min_value=0.0, format="%.4f")
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            st.success(f"✅ Data disimpan:\n- Waktu: {waktu}\n- Konsentrasi: {konsentrasi}")
