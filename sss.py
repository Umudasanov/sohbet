import streamlit as st
import os

CHAT_FILE = "chat.txt"

st.title("Bizim Gizli Çat")

# İstifadəçinin giriş vəziyyətini yadda saxlamaq üçün
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Giriş ekranı (Əgər hələ daxil olunmayıbsa)
if not st.session_state.logged_in:
    st.subheader("Giriş")
    user_select = st.selectbox("Adınızı seçin:", ["Umud", "Alis"])
    password = st.text_input("Gizli şifrəni daxil edin:", type="password")
    
    if st.button("Daxil ol"):
        if password == "umudalis": # Şifrəni bura qoy
            st.session_state.logged_in = True
            st.session_state.username = user_select
            st.rerun()
        else:
            st.error("Şifrə yanlışdır!")
else:
    # Çat ekranı (Giriş edildikdən sonra)
    st.write(f"Salam, **{st.session_state.username}**!")
    
    # Çıxış düyməsi
    if st.sidebar.button("Çıxış"):
        st.session_state.logged_in = False
        st.rerun()

    # Mesaj göndərmə
    msg = st.text_input("Mesajınız:", key="msg_input")
    if st.button("Göndər"):
        if msg:
            with open(CHAT_FILE, "a", encoding="utf-8") as f:
                f.write(f"{st.session_state.username}: {msg}\n")
            st.rerun()

    # Mesajları göstərmə
    st.markdown("---")
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            messages = f.readlines()
            for m in reversed(messages[-20:]):
                st.text(m.strip())
