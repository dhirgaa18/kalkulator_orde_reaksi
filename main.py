import streamlit as st

st.markdown("<h1 style='text-align: center;'>Orde Reaction Calculator</h1>", unsafe_allow_html=True)

if st.button("Tambahkan Data"):
    st.session_state.show_form = not st.session_state.show_form
