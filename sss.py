import streamlit as st
import os

CHAT_FILE = "chat.txt"

st.set_page_config(page_title="Bizim Çat", page_icon="💬")
st.title("💬 Gizli Çat")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Giriş Ekranı
if not st.session_state.logged_in:
    user_select = st.selectbox("Adınızı seçin:", ["Umud", "Alis"])
    password = st.text_input("Gizli şifrə:", type="password")
    if st.button("Daxil ol"):
        if password == "umudalis":
            st.session_state.logged_in = True
            st.session_state.username = user_select
            st.rerun()
        else:
            st.error("Şifrə yanlışdır!")
else:
    st.sidebar.write(f"Siz: **{st.session_state.username}**")
    
    # Yeniləmə düyməsi
    if st.button("🔄 Söhbəti Yenilə"):
        st.rerun()

    # Mesajları göstərmə (WhatsApp stili)
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            messages = f.readlines()
            for m in messages:
                if ":" in m:
                    sender, content = m.split(":", 1)
                    sender = sender.strip()
                    content = content.strip()

                    # Məntiq: Əgər mesajı mən yazmışamsa, rolu 'user' (sağ) et
                    # Yox, qarşı tərəf yazıbsa, rolu 'assistant' (sol) et
                    role = "user" if sender == st.session_state.username else "assistant"
                    
                    with st.chat_message(role):
                        st.write(f"**{sender}**: {content}")

    # Yeni mesaj yazmaq
    if prompt := st.chat_input("Mesajını yaz..."):
        with open(CHAT_FILE, "a", encoding="utf-8") as f:
            f.write(f"{st.session_state.username}: {prompt}\n")
        st.rerun()

    if st.sidebar.button("Çıxış"):
        st.session_state.logged_in = False
        st.rerun()
