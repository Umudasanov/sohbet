import streamlit as st
import os

CHAT_FILE = "chat.txt"

st.title("Bizim Gizli Çat")

# Şifrə sistemi
password = st.text_input("Gizli açar:", type="password")

if password == "umudalis": 
    st.success("Xoş gəldin!")
    
    # 1. Mesajı göndərmə hissəsi
    msg = st.text_input("Mesajını yaz:", key="msg_input")
    if st.button("Göndər"):
        if msg:  # Boş mesaj göndərməsin
            with open(CHAT_FILE, "a", encoding="utf-8") as f:
                f.write(f"Umud/Fəridə: {msg}\n")
            st.rerun() # <-- ƏN VACİB HİSSƏ: Bu, səhifəni yeniləyir
    
    # 2. Mesajları oxuma və göstərmə hissəsi
    st.markdown("---")
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            messages = f.readlines()
            # Son 20 mesajı aşağıdan yuxarıya doğru göstər
            for m in reversed(messages[-20:]):
                st.write(m)
else:
    st.warning("Düzgün şifrə daxil edin.")
