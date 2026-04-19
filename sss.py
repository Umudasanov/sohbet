import streamlit as st

st.title("Gizli Söhbət")

# Şifrə sistemi
password = st.text_input("Gizli açarı daxil edin:", type="password")

if password == "1234":  # Öz şifrəni bura yaz
    st.success("Daxil oldunuz!")
    msg = st.text_input("Mesajınız:")
    if st.button("Göndər"):
        st.write(f"Siz: {msg}")
else:
    st.warning("Zəhmət olmasa düzgün açarı daxil edin.")
