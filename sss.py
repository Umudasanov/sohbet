import streamlit as st
import os
import json
import uuid
import shutil
from datetime import datetime

# Qovluqlar və fayl
DATA_FILE = "chat.json"
MEDIA_DIR = "media"

if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

# Məlumatları yüklə/yadda saxla
def load_data():
    if not os.path.exists(DATA_FILE): return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

st.set_page_config(page_title="Bizim Çat", page_icon="💬")
st.title("💬 Gizli Çat v2.0")

# Sessiya idarəsi
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.hidden_msgs = [] # Özü üçün sildiyi mesajlar

# --- GİRİŞ ---
if not st.session_state.logged_in:
    name = st.selectbox("Adınız:", ["Umud", "Alis"])
    if st.button("Daxil ol"):
        st.session_state.logged_in = True
        st.session_state.user = name
        st.rerun()
else:
    # --- SİLİNMƏ MƏNTİQİ ---
    messages = load_data()
    
    # 1. Çatı hamı üçün təmizlə
    if st.sidebar.button("🗑 Söhbəti tam sil (Hər kəs üçün)"):
        save_data([]) # Faylı boşalt
        st.rerun()

    # --- MESAJLARIN GÖSTƏRİLMƏSİ ---
    for msg in messages:
        # Əgər mesaj "mənə" görə gizlədilibsə, göstərmə
        if msg['id'] in st.session_state.hidden_msgs:
            continue

        role = "user" if msg['sender'] == st.session_state.user else "assistant"
        with st.chat_message(role):
            st.write(f"**{msg['sender']}**: {msg['text']}")
            
            # Media varsa göstər
            if msg['media_path']:
                if msg['type'] == 'image': st.image(msg['media_path'])
                elif msg['type'] == 'video': st.video(msg['media_path'])
                elif msg['type'] == 'audio': st.audio(msg['media_path'])

            # Silmə düymələri
            col1, col2 = st.columns(2)
            if col1.button("❌ Hər kəsdən sil", key=f"del_all_{msg['id']}"):
                messages = [m for m in messages if m['id'] != msg['id']]
                save_data(messages)
                st.rerun()
            if col2.button("🚫 Yalnız məndən gizlət", key=f"del_me_{msg['id']}"):
                st.session_state.hidden_msgs.append(msg['id'])
                st.rerun()

    # --- MESAJ GÖNDƏRMƏ ---
    prompt = st.chat_input("Mesaj və ya fayl...")
    uploaded_file = st.file_uploader("Fayl seç (Şəkil, Video, Səs)", type=['png', 'jpg', 'mp4', 'mp3'])

    if prompt or uploaded_file:
        media_path = None
        media_type = None

        if uploaded_file:
            ext = uploaded_file.name.split('.')[-1]
            media_path = os.path.join(MEDIA_DIR, f"{uuid.uuid4()}.{ext}")
            with open(media_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            if ext in ['png', 'jpg']: media_type = 'image'
            elif ext == 'mp4': media_type = 'video'
            elif ext == 'mp3': media_type = 'audio'

        new_msg = {
            "id": str(uuid.uuid4()),
            "sender": st.session_state.user,
            "text": prompt or "",
            "media_path": media_path,
            "type": media_type
        }
        messages.append(new_msg)
        save_data(messages)
        st.rerun()
