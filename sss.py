import streamlit as st
import os
import json
import uuid
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- REAL-TIME AYARI ---
# Hər 1 saniyədə səhifəni avtomatik yeniləyir
st_autorefresh(interval=1000, key="datarefresh")

# Fayllar
DATA_FILE = "chat.json"
MEDIA_DIR = "media"

if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

def load_data():
    if not os.path.exists(DATA_FILE): return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

st.set_page_config(page_title="Bizim Çat", page_icon="💬")
st.title("💬 Gizli Çat v2.0")

# --- SESSİYA İDARƏSİ ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.session_state.hidden_msgs = [] 

# --- GİRİŞ ---
if not st.session_state.logged_in:
    name = st.selectbox("Adınız:", ["Umud", "Alis"])
    password = st.text_input("Şifrə:", type="password")
    if st.button("Daxil ol"):
        if password == "umudalis":
            st.session_state.logged_in = True
            st.session_state.user = name
            st.rerun()
        else: st.error("Şifrə yanlışdır!")
else:
    # --- SİLİNMƏ ---
    if st.sidebar.button("🗑 Söhbəti təmizlə"):
        save_data([])
        st.rerun()

    messages = load_data()

    # --- MESAJLARIN GÖSTƏRİLMƏSİ ---
    for msg in messages:
        if msg['id'] in st.session_state.hidden_msgs: continue

        role = "user" if msg['sender'] == st.session_state.user else "assistant"
        
        with st.chat_message(role):
            st.write(f"**{msg['sender']}**: {msg['text']}")
            
            if msg['media_path'] and os.path.exists(msg['media_path']):
                if msg['type'] == 'image': st.image(msg['media_path'])
                elif msg['type'] == 'video': st.video(msg['media_path'])
                elif msg['type'] == 'audio': st.audio(msg['media_path'])

            st.caption(f"{msg['time']}  ✅")

            if st.button("Sil", key=f"del_{msg['id']}"):
                messages = [m for m in messages if m['id'] != msg['id']]
                save_data(messages)
                st.rerun()

    # --- MESAJ GÖNDƏRMƏ ---
    prompt = st.chat_input("Mesaj yaz...")
    uploaded_file = st.file_uploader("Fayl əlavə et", type=['png', 'jpg', 'mp4', 'mp3'])

    if prompt or uploaded_file:
        media_path = None
        media_type = None

        if uploaded_file:
            ext = uploaded_file.name.split('.')[-1]
            media_path = os.path.join(MEDIA_DIR, f"{uuid.uuid4()}.{ext}")
            with open(media_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            media_type = 'image' if ext in ['png', 'jpg'] else 'video' if ext == 'mp4' else 'audio'

        new_msg = {
            "id": str(uuid.uuid4()),
            "sender": st.session_state.user,
            "text": prompt or "",
            "media_path": media_path,
            "type": media_type,
            "time": datetime.now().strftime("%H:%M")
        }
        messages.append(new_msg)
        save_data(messages)
        st.rerun()
