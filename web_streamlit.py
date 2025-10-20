# web_streamlit.py
import streamlit as st
import requests
import time

st.set_page_config(page_title="Theo dõi Vote Real-Time", layout="centered")
st.title("📊 Theo dõi tỷ lệ bình chọn (Realtime)")

# Thay bằng đường dẫn raw tới data.json trong repo của bạn:
GITHUB_USER = "ngan95025-dotcom"
REPO = "vote-monitor"
BRANCH = "main"
RAW_URL = f"https://raw.githubusercontent.com/ngan95025-dotcom/vote-monitor/main/data.json"

placeholder = st.empty()
poll_interval = 3  # giây giữa các lần fetch

def fetch_json():
    try:
        r = requests.get(RAW_URL, timeout=5)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None

last_ts = None
while True:
    data = fetch_json()
    with placeholder.container():
        if not data:
            st.info("⏳ Chưa có dữ liệu hoặc đang chờ cập nhật...")
        else:
            ts = data.get("timestamp", "N/A")
            st.markdown(f"### 🕒 Cập nhật: `{ts}`")
            if data.get("rank"):
                st.markdown(f"**🏅 Xếp hạng:** {data.get('rank')}")
            st.subheader("📊 Dữ liệu hiện tại:")
            table_data = []
            candidates = data.get("candidates", {})
            deltas = data.get("deltas", {})
            for name, val in candidates.items():
                table_data.append({
                    "Thí sinh": name,
                    "Tỷ lệ (%)": f"{val:.4f}" if val is not None else "-",
                    "Thay đổi (Δ)": f"{deltas.get(name, '-')}"
                })
            st.table(table_data)
    time.sleep(poll_interval)
