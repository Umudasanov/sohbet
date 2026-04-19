import streamlit as st
import os
from streamlit_autorefresh import st_autorefresh

# --- ƏN VACİB HİSSƏ: Avtomatik yenilənməni ən başa qoyuruq ---
st_autorefresh(interval=1000, key="datarefresh") # 1 saniyədə bir yenilənir

CHAT_FILE = "chat.txt"

st.set_page_config(page_title="Bizim Çat", page_icon="💬")
st.title("💬 Gizli Çat")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Giriş Ekranı
if not st.session_state.logged_in:
    user_select = st.selectbox("İstifadəçi seçin:", ["Umud", "Alis"])
    password = st.text_input("Gizli şifrə:", type="password")
    if st.button("Daxil ol"):
        if password == "umudalis":
            st.session_state.logged_in = True
            st.session_state.username = user_select
            st.rerun()
        else:
            st.error("Şifrə yanlışdır!")
else:
    # --- Çat Ekranı ---
    # Mesajları oxumaq üçün funksiya
    def get_messages():
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                return f.readlines()
        return []

    # Mesajları göstərmə (WhatsApp stili)
    messages = get_messages()
    for m in messages:
        if ":" in m:
            sender, content = m.split(":", 1)
            sender = sender.strip()
            role = "user" if sender == st.session_state.username else "assistant"
            with st.chat_message(role):
                st.write(f"**{sender}**: {content.strip()}")

    # Yeni mesaj yazmaq
    if prompt := st.chat_input("Mesajını yaz..."):
        with open(CHAT_FILE, "a", encoding="utf-8") as f:
            f.write(f"{st.session_state.username}: {prompt}\n")
        st.rerun()

    if st.sidebar.button("Çıxış"):
        st.session_state.logged_in = False
        st.rerun()
